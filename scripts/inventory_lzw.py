#!/usr/bin/env python3
"""Decompress every .lzw in Koukai2/ and print a size-distribution inventory.

Helps infer per-file content: uniform part sizes → fixed-size sprite grids;
mixed sizes → variable-length records or multi-resolution images.
"""
from collections import Counter
from pathlib import Path

from ls11_decode import ls11_decode_parts

SRC = Path("/Users/dong/Projects/Koukai2")
REPO = Path(__file__).resolve().parent.parent
OUT_ROOT = REPO / "output" / "lzw_parts"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

# Skip ones we've already done
SKIP = {"Kao.lzw"}


def main():
    files = sorted(p for p in SRC.glob("*.lzw") if p.name not in SKIP)
    for f in files:
        data = f.read_bytes()
        magic = data[:4]
        try:
            parts = ls11_decode_parts(data)
        except Exception as e:
            print(f"\n{f.name:<16} magic={magic!r} ERROR: {e}")
            continue
        sizes = [len(p) for p in parts]
        ctr = Counter(sizes)
        topk = ctr.most_common(5)
        total = sum(sizes)
        print(
            f"\n{f.name:<16} magic={magic.decode(errors='replace'):<4} "
            f"parts={len(parts):>4} total={total:>9,}  "
            f"size_min={min(sizes):>6} size_max={max(sizes):>6}"
        )
        print(f"  top sizes: {topk}")
        # Write parts
        sub = OUT_ROOT / f.stem
        sub.mkdir(exist_ok=True)
        for i, p in enumerate(parts):
            (sub / f"part_{i:04d}_{len(p)}bytes.bin").write_bytes(p)


if __name__ == "__main__":
    main()
