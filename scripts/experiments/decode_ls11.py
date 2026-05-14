#!/usr/bin/env python3
"""KOEI LS11 / LS10 LZSS decompressor — multi-variant try.

Header inferred from hex inspection:
  bytes 0-3   : magic "LS11" (or "LS10")
  bytes 4-15  : reserved (all 0x00 in samples)
  bytes 16+   : compressed bit/byte stream

LS11 is KOEI's LZSS-family compression (太閤立志伝 / 信長の野望 / 大航海時代 II /
三国志 IV's MAINMAP.S4 all use it). Exact variant isn't fully standardised
across versions, so we try the common parameter combinations and report
output sizes for visual inspection.

Variants:
  A: byte flags, bit=1 literal,    offset = b1 | ((b2 & 0xF0) << 4),
                                   length = (b2 & 0x0F) + 3
  B: byte flags, bit=0 literal,    same offset/length encoding
  C: byte flags, bit=1 literal,    offset = (b1 << 4) | (b2 >> 4),
                                   length = (b2 & 0x0F) + 3
  D: byte flags, bit=1 literal,    offset = b1 | ((b2 & 0xF0) << 4),
                                   length = (b2 & 0x0F) + 2   (different min)

Window initialized to 0x00 (common in KOEI tools).
Reads bits LSB first within each flag byte.
"""
import struct
import sys
from pathlib import Path

SRC_DIR = Path("/Users/dong/Projects/Koukai2")
OUT_DIR = Path("/Users/dong/Projects/sea2_demo/output/decompressed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADER_SIZE = 16
WIN_SIZE = 4096


def variant_decode(data: bytes, *, lit_bit: int, offset_form: str,
                   min_match: int, max_out: int = 4_000_000) -> bytes:
    """Generic LZSS decoder with knobs."""
    out = bytearray()
    window = bytearray(WIN_SIZE)
    win_pos = 0
    i = HEADER_SIZE
    n = len(data)

    while i < n and len(out) < max_out:
        if i >= n:
            break
        flag = data[i]
        i += 1
        for bit in range(8):
            if i >= n or len(out) >= max_out:
                break
            is_literal = ((flag >> bit) & 1) == lit_bit
            if is_literal:
                byte = data[i]
                i += 1
                out.append(byte)
                window[win_pos] = byte
                win_pos = (win_pos + 1) % WIN_SIZE
            else:
                if i + 1 >= n:
                    return bytes(out)
                b1 = data[i]
                b2 = data[i + 1]
                i += 2
                if offset_form == "lo_hi4":
                    offset = b1 | ((b2 & 0xF0) << 4)
                    length = (b2 & 0x0F) + min_match
                elif offset_form == "hi_lo4":
                    offset = (b1 << 4) | (b2 >> 4)
                    length = (b2 & 0x0F) + min_match
                else:
                    raise ValueError(offset_form)
                # bounds-check offset
                offset &= 0x0FFF
                for j in range(length):
                    byte = window[(offset + j) % WIN_SIZE]
                    out.append(byte)
                    window[win_pos] = byte
                    win_pos = (win_pos + 1) % WIN_SIZE
                    if len(out) >= max_out:
                        break
    return bytes(out)


def quality_score(data: bytes) -> dict:
    """Stats to spot a successful decode without looking at images.

    A good decompression typically has:
    - reasonable size (not too small / not absurdly large)
    - varied bytes (not all-zero, not all-FF)
    - moderate entropy (real data, not noise)
    """
    if not data:
        return {"len": 0, "unique": 0, "max_run": 0, "zero_ratio": 0}
    unique = len(set(data))
    # Longest run of identical bytes
    max_run = 1
    cur_run = 1
    for k in range(1, len(data)):
        if data[k] == data[k - 1]:
            cur_run += 1
            if cur_run > max_run:
                max_run = cur_run
        else:
            cur_run = 1
    zero_ratio = data.count(0) / len(data)
    return {
        "len": len(data),
        "unique": unique,
        "max_run": max_run,
        "zero_ratio": round(zero_ratio, 3),
    }


def try_file(src: Path) -> None:
    data = src.read_bytes()
    print(f"=== {src.name} ===")
    print(f"  size: {len(data):,} bytes")
    print(f"  magic: {data[:4]}")
    print(f"  next-12 (should be zeros): {data[4:16].hex()}")
    print(f"  first compressed bytes: {data[16:24].hex()}")
    print()

    variants = [
        ("A_lit1_lohi4_min3", dict(lit_bit=1, offset_form="lo_hi4", min_match=3)),
        ("B_lit0_lohi4_min3", dict(lit_bit=0, offset_form="lo_hi4", min_match=3)),
        ("C_lit1_hilo4_min3", dict(lit_bit=1, offset_form="hi_lo4", min_match=3)),
        ("D_lit1_lohi4_min2", dict(lit_bit=1, offset_form="lo_hi4", min_match=2)),
        ("E_lit0_lohi4_min2", dict(lit_bit=0, offset_form="lo_hi4", min_match=2)),
        ("F_lit0_hilo4_min3", dict(lit_bit=0, offset_form="hi_lo4", min_match=3)),
    ]

    base = src.stem
    for name, kwargs in variants:
        try:
            decoded = variant_decode(data, **kwargs)
        except Exception as e:
            print(f"  {name}: ERROR {e}")
            continue
        out_path = OUT_DIR / f"{base}_{name}.bin"
        out_path.write_bytes(decoded)
        q = quality_score(decoded)
        print(f"  {name}: len={q['len']:>8,}  unique={q['unique']:>3}  "
              f"max_run={q['max_run']:>5}  zero_ratio={q['zero_ratio']}")
    print()


def main():
    targets = ["Kao.lzw", "Char.lzw", "Data1.lzw"]
    for t in targets:
        path = SRC_DIR / t
        if not path.exists():
            print(f"[skip] {t}")
            continue
        try_file(path)

    print(f"All variants written → {OUT_DIR}")
    print("Check sizes: the right variant typically has len 2-5x the compressed size,")
    print("unique ~ 256 (full byte range), max_run small (no runaway loops).")


if __name__ == "__main__":
    main()
