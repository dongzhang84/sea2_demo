#!/usr/bin/env python3
"""Render decoded Kao parts as PNG.

Each part is a 4-plane PC-98 planar bitmap, 64 px wide.
Height varies per part (size / 32 bytes-per-scanline).
Layout: interleaved per scanline (4 planes × 8 bytes per row).
"""
from pathlib import Path
from PIL import Image

PARTS = Path("/Users/dong/Projects/sea2_demo/output/kao_parts")
OUT = Path("/Users/dong/Projects/sea2_demo/output/kao_png")
OUT.mkdir(parents=True, exist_ok=True)

# A reasonable 16-color skin-tone-ish palette so faces are visible
# (PC-98 actual palette is in MAIN.EXE; this is a placeholder for visibility)
PALETTE = [
    (0, 0, 0),         # 0 black
    (40, 40, 40),      # 1 dark
    (200, 160, 130),   # 2 skin
    (160, 100, 60),    # 3 darker skin
    (80, 50, 30),      # 4 hair brown
    (220, 200, 170),   # 5 light skin
    (255, 255, 255),   # 6 white
    (180, 180, 180),   # 7 light gray
    (30, 30, 100),     # 8 dark blue
    (200, 50, 50),     # 9 red
    (50, 130, 50),     # 10 green
    (100, 100, 100),   # 11 gray
    (140, 120, 90),    # 12 tan
    (90, 60, 40),      # 13 brown
    (240, 180, 120),   # 14 light tan
    (255, 220, 200),   # 15 highlight
]


def planar_to_indexed(data: bytes, w: int, h: int) -> list[int]:
    """4-plane planar bitmap → flat indexed pixel list.
    Layout: for each scanline, 4 planes of (w/8) bytes concatenated.
    """
    bytes_per_plane_row = w // 8
    expected = bytes_per_plane_row * 4 * h
    if len(data) < expected:
        data = data + b"\x00" * (expected - len(data))
    pixels = []
    for y in range(h):
        row_start = y * bytes_per_plane_row * 4
        for x in range(w):
            byte_idx = x >> 3
            bit_idx = 7 - (x & 7)
            idx = 0
            for plane in range(4):
                b = data[row_start + plane * bytes_per_plane_row + byte_idx]
                if b & (1 << bit_idx):
                    idx |= 1 << plane
            pixels.append(idx)
    return pixels


def main():
    parts = sorted(PARTS.glob("part_*.bin"))
    print(f"Rendering {len(parts)} parts")

    # Build palette flat
    pal = []
    for r, g, b in PALETTE:
        pal.extend([r, g, b])
    pal += [0] * (768 - len(pal))

    rendered = 0
    for part_path in parts:
        size = part_path.stat().st_size
        # Height = bytes / 32 bytes-per-scanline (64 px × 4 planes / 8)
        height = size // 32
        if height < 8 or height > 200:
            continue
        data = part_path.read_bytes()
        pixels = planar_to_indexed(data, 64, height)

        img = Image.new("P", (64, height))
        img.putdata(pixels)
        img.putpalette(pal)
        # Upscale 4x for visibility
        img.resize((64 * 4, height * 4), Image.NEAREST).save(
            OUT / f"{part_path.stem}.png"
        )
        rendered += 1

    print(f"Wrote {rendered} PNGs → {OUT}")

    # Also build a contact sheet
    print("Building contact sheet...")
    all_pngs = sorted(OUT.glob("*.png"))
    if not all_pngs:
        return
    # Grid: 16 columns
    cols = 16
    rows = (len(all_pngs) + cols - 1) // cols
    thumb_w, thumb_h = 64, 80
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 30))
    for i, p in enumerate(all_pngs):
        img = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), Image.NEAREST)
        cx = (i % cols) * thumb_w
        cy = (i // cols) * thumb_h
        sheet.paste(img, (cx, cy))
    sheet.save(OUT.parent / "kao_contact_sheet.png")
    print(f"Contact sheet → {OUT.parent / 'kao_contact_sheet.png'}")


if __name__ == "__main__":
    main()
