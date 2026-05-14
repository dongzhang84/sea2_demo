#!/usr/bin/env python3
"""Bit-aligned LZSS — last reasonable hypothesis before falling back to
disassembling DKK2E.exe.

Format per token:
  1 bit: literal flag
    if literal: 8 bits = literal byte
    if reference: offset_bits + length_bits
      length = stored + min_match

Variants tried sweep:
  bit order (MSB/LSB), literal_flag value (0 or 1),
  offset_bits (11/12/13), length_bits (3/4), min_match (2/3)

A 'plausible' decode: output length 2-5x input, byte variety ~256,
no tiny output (<100 bytes means decoder bailed immediately).
"""
from pathlib import Path
from itertools import product

SRC = Path("/Users/dong/Projects/Koukai2/Kao.lzw")
OUT_DIR = Path("/Users/dong/Projects/sea2_demo/output/decompressed_bitlzss")
OUT_DIR.mkdir(parents=True, exist_ok=True)


class BitReader:
    def __init__(self, data: bytes, msb_first: bool):
        self.data = data
        self.pos = 0
        self.msb = msb_first
        self.nbits = len(data) * 8

    def read(self, n: int) -> int | None:
        if self.pos + n > self.nbits:
            return None
        v = 0
        if self.msb:
            for _ in range(n):
                b = self.data[self.pos >> 3]
                bit = (b >> (7 - (self.pos & 7))) & 1
                v = (v << 1) | bit
                self.pos += 1
        else:
            for i in range(n):
                b = self.data[self.pos >> 3]
                bit = (b >> (self.pos & 7)) & 1
                v |= bit << i
                self.pos += 1
        return v


def decode(data: bytes, header: int, msb: bool, lit_flag: int,
           off_bits: int, len_bits: int, min_match: int,
           win_size: int = 4096, max_out: int = 4_000_000) -> bytes:
    br = BitReader(data[header:], msb_first=msb)
    out = bytearray()
    window = bytearray(win_size)
    win_pos = 0

    while len(out) < max_out:
        flag = br.read(1)
        if flag is None:
            break
        if flag == lit_flag:
            b = br.read(8)
            if b is None:
                break
            out.append(b)
            window[win_pos] = b
            win_pos = (win_pos + 1) % win_size
        else:
            off = br.read(off_bits)
            ln = br.read(len_bits)
            if off is None or ln is None:
                break
            length = ln + min_match
            off &= win_size - 1
            for j in range(length):
                b = window[(off + j) % win_size]
                out.append(b)
                window[win_pos] = b
                win_pos = (win_pos + 1) % win_size
                if len(out) >= max_out:
                    break
    return bytes(out)


def main():
    data = SRC.read_bytes()
    print(f"Source: {SRC.name}  ({len(data):,} bytes)")
    print()

    results = []
    # Sweep parameters
    for header in (4, 8, 16):
        for msb in (True, False):
            for lit_flag in (0, 1):
                for off_bits in (11, 12, 13):
                    for len_bits in (3, 4):
                        for min_match in (2, 3):
                            win = 1 << off_bits
                            try:
                                out = decode(data, header, msb, lit_flag,
                                             off_bits, len_bits, min_match,
                                             win_size=win)
                            except Exception:
                                continue
                            results.append((
                                len(out), header, msb, lit_flag,
                                off_bits, len_bits, min_match, out
                            ))

    # Sort by len descending, show top 15 plausible (size > 100K)
    print(f"Tried {len(results)} variants. Top 15 by decoded size:")
    results.sort(key=lambda r: -r[0])
    for i, (ln, hdr, msb, lf, ob, lb, mm, out) in enumerate(results[:15]):
        msb_s = "MSB" if msb else "LSB"
        unique = len(set(out)) if out else 0
        name = f"hdr{hdr}_{msb_s}_lit{lf}_off{ob}_len{lb}_min{mm}"
        path = OUT_DIR / f"Kao_{name}.bin"
        path.write_bytes(out)
        print(f"  {i+1:2d}. len={ln:>9,}  unique={unique:>3}  {name}")

    # Also save a few of the smaller ones as control
    print(f"\nAlso saving 3 mid-size variants for reference...")
    mid_idx = len(results) // 2
    for i in range(mid_idx, mid_idx + 3):
        if i >= len(results):
            break
        ln, hdr, msb, lf, ob, lb, mm, out = results[i]
        msb_s = "MSB" if msb else "LSB"
        name = f"hdr{hdr}_{msb_s}_lit{lf}_off{ob}_len{lb}_min{mm}"
        (OUT_DIR / f"Kao_{name}.bin").write_bytes(out)
        print(f"  mid: len={ln:>9,}  {name}")


if __name__ == "__main__":
    main()
