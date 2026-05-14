#!/usr/bin/env python3
"""Render Portchip.lzw using JohanLi's tileset_regular encoding.

Discovered from github.com/JohanLi/uncharted-waters-2-research:
  - 16×16 tiles, 4 bits per pixel (16 colors)
  - 1024-bit blocks: each block = 256 pixels of one tile
  - Within a block, pixel i takes bits [block[i], block[i+256], block[i+512], block[i+768]]
    concatenated MSB-first
  - 16-color palette has day/night/dusk/dawn variants (we use "day")

Portchip has 7 big parts × 30720 B = 240 tiles per part (1680 total) +
7 small 4-byte parts (probably sub-palette indices into a master palette).
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PARTS = REPO / "output" / "lzw_parts" / "Portchip"
OUT = REPO / "output" / "portchip_v2"
OUT.mkdir(parents=True, exist_ok=True)

PALETTE_DAY = {
    0: "000000", 1: "717192", 2: "888888", 3: "0082F3", 4: "D34100",
    5: "A26100", 6: "F3A261", 7: "00B261", 8: "0041D3", 9: "0041C3",
    10: "00A2F3", 11: "007161", 12: "888888", 13: "E3B251", 14: "F3E3D3",
    15: "F3E3D3",
}
PALETTE = np.array(
    [tuple(int(PALETTE_DAY[k][i:i + 2], 16) for i in (0, 2, 4)) for k in range(16)],
    dtype=np.uint8,
)

TILE_W = TILE_H = 16
BPP = 4
BLOCK_BITS = TILE_W * TILE_H * BPP  # 1024
PIXELS_PER_BLOCK = BLOCK_BITS // BPP  # 256
TILE_BYTES = BLOCK_BITS // 8  # 128


def decode_part(raw: bytes) -> np.ndarray:
    """Decode a 30720-byte Portchip part → (240, 16, 16, 3) numpy array."""
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    n_blocks = len(bits) // BLOCK_BITS
    tiles = np.zeros((n_blocks, TILE_H, TILE_W, 3), dtype=np.uint8)
    for b in range(n_blocks):
        block = bits[b * BLOCK_BITS:(b + 1) * BLOCK_BITS]
        for i in range(PIXELS_PER_BLOCK):
            p = (
                (int(block[i]) << 3)
                | (int(block[i + 256]) << 2)
                | (int(block[i + 512]) << 1)
                | int(block[i + 768])
            )
            y, x = divmod(i, TILE_W)
            tiles[b, y, x] = PALETTE[p]
    return tiles


def main():
    bigs = sorted([p for p in PARTS.glob("*.bin") if p.stat().st_size == 30720])
    print(f"decoding {len(bigs)} Portchip parts × 240 tiles each")

    all_tiles = []
    for p in bigs:
        tiles = decode_part(p.read_bytes())
        all_tiles.append(tiles)

    # One contact sheet per part: 16 cols × 15 rows of 16×16 tiles, 3× scale
    SCALE = 3
    cols = 16
    for idx, tiles in enumerate(all_tiles):
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new(
            "RGB",
            (cols * TILE_W * SCALE, rows * TILE_H * SCALE),
            (40, 40, 60),
        )
        for i, t in enumerate(tiles):
            r, c = divmod(i, cols)
            tile_img = Image.fromarray(t, "RGB").resize(
                (TILE_W * SCALE, TILE_H * SCALE), Image.NEAREST
            )
            sheet.paste(tile_img, (c * TILE_W * SCALE, r * TILE_H * SCALE))
        out_path = OUT / f"part{idx}_atlas.png"
        sheet.save(out_path)
        print(f"  → {out_path.name} ({out_path.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
