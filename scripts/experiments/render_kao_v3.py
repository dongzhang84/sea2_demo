#!/usr/bin/env python3
"""v3 — width 32 chunky 4bpp confirmed partial-correct. Refine:

  A. width 32 chunky, proper variable height per part (no contact-sheet
     stretch). Render each at its native size.
  B. Test "left half + right half" theory: pair part[i] with part[i+128]
     side by side as 64-wide composite (i=0..127).
  C. Test "left + right interleave per row" theory: each part has
     left and right halves interleaved per scanline within the part.
  D. Width 32 chunky, only first half of bytes per part — to see if
     a single half-portrait is in there alone.
"""
from pathlib import Path
from PIL import Image

PARTS = Path("/Users/dong/Projects/sea2_demo/output/kao_parts")
OUT = Path("/Users/dong/Projects/sea2_demo/output/kao_png_v3")
OUT.mkdir(parents=True, exist_ok=True)

PAL16 = [
    (0, 0, 0), (40, 40, 40), (200, 160, 130), (160, 100, 60),
    (80, 50, 30), (220, 200, 170), (255, 255, 255), (180, 180, 180),
    (30, 30, 100), (200, 50, 50), (50, 130, 50), (100, 100, 100),
    (140, 120, 90), (90, 60, 40), (240, 180, 120), (255, 220, 200),
]


def chunky_pixels(data: bytes, hi_first: bool = True) -> list[int]:
    """Decode chunky 4bpp bytes to pixel list."""
    px = []
    for b in data:
        if hi_first:
            px.append((b >> 4) & 0xF)
            px.append(b & 0xF)
        else:
            px.append(b & 0xF)
            px.append((b >> 4) & 0xF)
    return px


def save(pixels, w, h, path, scale=3):
    img = Image.new("P", (w, h))
    img.putdata(pixels[:w * h])
    pal = [c for rgb in PAL16 for c in rgb] + [0] * (768 - 48)
    img.putpalette(pal)
    img.resize((w * scale, h * scale), Image.NEAREST).save(path)


def make_sheet(folder: Path, glob: str, name: str, thumb_w: int, thumb_h: int, cols: int = 16):
    pngs = sorted(folder.glob(glob))
    if not pngs:
        return
    rows = (len(pngs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 30))
    for i, p in enumerate(pngs):
        img = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), Image.NEAREST)
        cx = (i % cols) * thumb_w
        cy = (i // cols) * thumb_h
        sheet.paste(img, (cx, cy))
    out_path = folder.parent / f"contact_{name}.png"
    sheet.save(out_path)
    print(f"  contact: {out_path}")


def main():
    parts = sorted(PARTS.glob("part_*.bin"))
    print(f"v3: refining width-32 chunky on {len(parts)} parts")

    # A. Native-height width-32 chunky, hi nibble first (best so far)
    dir_a = OUT / "A_native_w32"
    dir_a.mkdir(exist_ok=True)
    for i, part in enumerate(parts):
        data = part.read_bytes()
        pixels = chunky_pixels(data, hi_first=True)
        h = len(pixels) // 32
        if h < 4:
            continue
        save(pixels, 32, h, dir_a / f"{i:04d}.png", scale=3)

    # B. Left/right pairing: part[i] = left, part[i+128] = right, combine 64×h
    dir_b = OUT / "B_paired_lr"
    dir_b.mkdir(exist_ok=True)
    for i in range(min(128, len(parts) // 2)):
        left_data = parts[i].read_bytes()
        right_data = parts[i + 128].read_bytes()
        left = chunky_pixels(left_data)
        right = chunky_pixels(right_data)
        h = min(len(left), len(right)) // 32
        if h < 4:
            continue
        # Combine row by row
        combined = []
        for y in range(h):
            combined.extend(left[y * 32:(y + 1) * 32])
            combined.extend(right[y * 32:(y + 1) * 32])
        save(combined, 64, h, dir_b / f"{i:04d}_paired.png", scale=3)

    # C. Single part split: left = first half pixels, right = second half pixels
    dir_c = OUT / "C_split_inside"
    dir_c.mkdir(exist_ok=True)
    for i, part in enumerate(parts):
        data = part.read_bytes()
        half = len(data) // 2
        left_data = data[:half]
        right_data = data[half:half * 2]
        left = chunky_pixels(left_data)
        right = chunky_pixels(right_data)
        h = min(len(left), len(right)) // 32
        if h < 4:
            continue
        combined = []
        for y in range(h):
            combined.extend(left[y * 32:(y + 1) * 32])
            combined.extend(right[y * 32:(y + 1) * 32])
        save(combined, 64, h, dir_c / f"{i:04d}_split.png", scale=3)

    # Contact sheets
    print("\nBuilding contact sheets...")
    make_sheet(dir_a, "*.png", "A_native_w32", 32 * 3, 60 * 3)
    make_sheet(dir_b, "*.png", "B_paired_lr", 64 * 3, 60 * 3)
    make_sheet(dir_c, "*.png", "C_split_inside", 64 * 3, 60 * 3)

    print(f"\n→ {OUT}")


if __name__ == "__main__":
    main()
