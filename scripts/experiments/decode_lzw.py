#!/usr/bin/env python3
"""Real LZW decoder (variable-width bit-packed codes) — multi-variant try.

The .lzw extension was the clue we missed. KOEI's LS11/LS10 is a true LZW
(Lempel-Ziv-Welch dictionary algorithm), NOT byte-aligned LZSS.

LZW variants tried (a successful one prints sensible decoded length):
  v1  MSB-first bits, start 9-bit, no clear/end codes, max 12-bit
  v2  LSB-first bits, start 9-bit, no clear/end codes, max 12-bit
  v3  MSB-first, start 9-bit, max 13-bit
  v4  LSB-first, start 9-bit, max 13-bit
  v5  MSB-first, start 9-bit, clear=256 end=257, max 12-bit (GIF-style)
  v6  MSB-first, fixed 12-bit width, no growth
"""
from pathlib import Path

SRC_DIR = Path("/Users/dong/Projects/Koukai2")
OUT_DIR = Path("/Users/dong/Projects/sea2_demo/output/decompressed_lzw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HEADER_SIZE = 16


class BitReader:
    def __init__(self, data: bytes, msb_first: bool):
        self.data = data
        self.bit_pos = 0
        self.msb_first = msb_first

    def read(self, n: int) -> int | None:
        if self.bit_pos + n > len(self.data) * 8:
            return None
        result = 0
        if self.msb_first:
            for _ in range(n):
                byte = self.data[self.bit_pos >> 3]
                bit = (byte >> (7 - (self.bit_pos & 7))) & 1
                result = (result << 1) | bit
                self.bit_pos += 1
        else:
            for i in range(n):
                byte = self.data[self.bit_pos >> 3]
                bit = (byte >> (self.bit_pos & 7)) & 1
                result |= bit << i
                self.bit_pos += 1
        return result


def lzw_decode(data: bytes, msb_first: bool, start_width: int = 9,
               max_width: int = 12, clear_code: int | None = None,
               end_code: int | None = None,
               max_out: int = 4_000_000) -> bytes:
    """Generic LZW decoder."""
    br = BitReader(data[HEADER_SIZE:], msb_first=msb_first)

    def reset_dict():
        d = [bytes([i]) for i in range(256)]
        if clear_code is not None:
            while len(d) <= max(clear_code, end_code or 0):
                d.append(b"")
        return d, start_width

    dict_, width = reset_dict()
    out = bytearray()
    prev: bytes | None = None
    growth_threshold = 1 << width

    while len(out) < max_out:
        code = br.read(width)
        if code is None:
            break
        if clear_code is not None and code == clear_code:
            dict_, width = reset_dict()
            growth_threshold = 1 << width
            prev = None
            continue
        if end_code is not None and code == end_code:
            break

        if code < len(dict_):
            entry = dict_[code]
        elif code == len(dict_) and prev is not None:
            entry = prev + prev[:1]
        else:
            # Invalid code → variant is wrong
            break

        if not entry:
            break
        out.extend(entry)

        if prev is not None:
            dict_.append(prev + entry[:1])
            # Grow width if dictionary fills (do this BEFORE next read)
            if len(dict_) >= growth_threshold and width < max_width:
                width += 1
                growth_threshold = 1 << width

        prev = entry

    return bytes(out)


def quality(d: bytes) -> str:
    if not d:
        return "EMPTY"
    unique = len(set(d))
    zero = d.count(0)
    return f"len={len(d):>8,} unique={unique:>3} zero%={zero/len(d):.2f}"


def try_file(src: Path) -> None:
    data = src.read_bytes()
    print(f"=== {src.name} ({len(data):,} bytes) ===")

    variants = [
        ("v1_msb_9to12",        dict(msb_first=True,  start_width=9, max_width=12)),
        ("v2_lsb_9to12",        dict(msb_first=False, start_width=9, max_width=12)),
        ("v3_msb_9to13",        dict(msb_first=True,  start_width=9, max_width=13)),
        ("v4_lsb_9to13",        dict(msb_first=False, start_width=9, max_width=13)),
        ("v5_msb_gif_9to12",    dict(msb_first=True,  start_width=9, max_width=12,
                                     clear_code=256, end_code=257)),
        ("v5b_lsb_gif_9to12",   dict(msb_first=False, start_width=9, max_width=12,
                                     clear_code=256, end_code=257)),
        ("v6_msb_fixed12",      dict(msb_first=True,  start_width=12, max_width=12)),
        ("v6b_lsb_fixed12",     dict(msb_first=False, start_width=12, max_width=12)),
    ]

    base = src.stem
    for name, kwargs in variants:
        try:
            decoded = lzw_decode(data, **kwargs)
        except Exception as e:
            print(f"  {name}: ERROR {type(e).__name__} {e}")
            continue
        (OUT_DIR / f"{base}_{name}.bin").write_bytes(decoded)
        print(f"  {name}: {quality(decoded)}")
    print()


def main():
    for name in ["Kao.lzw", "Char.lzw", "Data1.lzw"]:
        p = SRC_DIR / name
        if p.exists():
            try_file(p)
    print(f"→ {OUT_DIR}")


if __name__ == "__main__":
    main()
