#!/usr/bin/env python3
"""Render 1.pat / 2.pat as font tileset images.

1.pat = 7213 tiles × 16×12 (1bpp, 24 bytes each)
2.pat = 6800 tiles × 16×16 (1bpp, 32 bytes each)

Output:
  - output/fonts/2pat_atlas.png — full 2.pat tileset (likely CJK font)
  - output/fonts/2pat_first256.png — first 256 glyphs, larger
  - output/fonts/1pat_atlas.png — full 1.pat tileset
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "fonts"
OUT.mkdir(parents=True, exist_ok=True)


def render_tileset(raw: bytes, tile_w: int, tile_h: int, cols: int = 64,
                   scale: int = 1, gap: int = 1) -> Image.Image:
    """Render with `gap` blank pixels between tiles so glyphs don't bleed."""
    bytes_per_row = (tile_w + 7) // 8
    tile_bytes = bytes_per_row * tile_h
    n = len(raw) // tile_bytes
    rows = (n + cols - 1) // cols

    cell_w = tile_w + gap
    cell_h = tile_h + gap
    img = np.zeros((rows * cell_h, cols * cell_w), dtype=np.uint8)
    for i in range(n):
        chunk = raw[i * tile_bytes:(i + 1) * tile_bytes]
        bits = np.unpackbits(np.frombuffer(chunk, dtype=np.uint8)).reshape(tile_h, bytes_per_row * 8)
        glyph = bits[:tile_h, :tile_w]
        r, c = divmod(i, cols)
        img[r * cell_h:r * cell_h + tile_h, c * cell_w:c * cell_w + tile_w] = glyph * 255
    pil = Image.fromarray(img, "L")
    if scale != 1:
        pil = pil.resize((img.shape[1] * scale, img.shape[0] * scale), Image.NEAREST)
    return pil


def main():
    p1 = Path('/Users/dong/Projects/Koukai2/1.pat').read_bytes()
    p2 = Path('/Users/dong/Projects/Koukai2/2.pat').read_bytes()
    print(f'1.pat = {len(p1)} bytes, 2.pat = {len(p2)} bytes')

    # 2.pat first 256 glyphs at 3x for inspection
    raw_256 = p2[:256 * 32]
    img = render_tileset(raw_256, 16, 16, cols=16, scale=3)
    p = OUT / "2pat_first256.png"
    img.save(p)
    print(f'  → {p.name} ({p.stat().st_size:,} B)')

    # 2.pat full atlas at 1x
    img = render_tileset(p2, 16, 16, cols=80, scale=1)
    p = OUT / "2pat_atlas.png"
    img.save(p)
    print(f'  → {p.name} ({p.stat().st_size:,} B)  6800 glyphs')

    # 1.pat first 256 glyphs (try 16×12)
    raw_256_1 = p1[:256 * 24]
    img = render_tileset(raw_256_1, 16, 12, cols=16, scale=3)
    p = OUT / "1pat_first256_16x12.png"
    img.save(p)
    print(f'  → {p.name} ({p.stat().st_size:,} B)')

    # Also try 12×16 interpretation
    img = render_tileset(raw_256_1, 12, 16, cols=16, scale=3)
    p = OUT / "1pat_first256_12x16.png"
    img.save(p)
    print(f'  → {p.name} ({p.stat().st_size:,} B)')


if __name__ == "__main__":
    main()
