#!/usr/bin/env python3
"""Re-render Kao parts trying multiple bitmap formats.

LS11 decoding is correct; the bug was the bitmap interpretation.
For each part, output 6 hypothesis renderings into output/kao_png_v2/.
Look at the contact sheets to see which hypothesis works.
"""
from pathlib import Path
from PIL import Image

PARTS = Path("/Users/dong/Projects/sea2_demo/output/kao_parts")
OUT = Path("/Users/dong/Projects/sea2_demo/output/kao_png_v2")
OUT.mkdir(parents=True, exist_ok=True)

# Simple skin-toned 16-color palette for visibility
PAL16 = [
    (0, 0, 0), (40, 40, 40), (200, 160, 130), (160, 100, 60),
    (80, 50, 30), (220, 200, 170), (255, 255, 255), (180, 180, 180),
    (30, 30, 100), (200, 50, 50), (50, 130, 50), (100, 100, 100),
    (140, 120, 90), (90, 60, 40), (240, 180, 120), (255, 220, 200),
]


def chunky_4bpp(data: bytes, w: int) -> tuple[list[int], int]:
    """Chunky 4-bit-per-pixel: each byte = 2 pixels (high nibble first)."""
    pixels = []
    for b in data:
        pixels.append((b >> 4) & 0xF)
        pixels.append(b & 0xF)
    h = len(pixels) // w
    return pixels[:w * h], h


def chunky_4bpp_lo_first(data: bytes, w: int) -> tuple[list[int], int]:
    """Same but low nibble first."""
    pixels = []
    for b in data:
        pixels.append(b & 0xF)
        pixels.append((b >> 4) & 0xF)
    h = len(pixels) // w
    return pixels[:w * h], h


def planar_4plane(data: bytes, w: int) -> tuple[list[int], int]:
    bpr = w // 8
    h = len(data) // (bpr * 4)
    pixels = []
    for y in range(h):
        for x in range(w):
            row_start = y * bpr * 4
            byte_idx = x >> 3
            bit_idx = 7 - (x & 7)
            idx = 0
            for plane in range(4):
                pos = row_start + plane * bpr + byte_idx
                if pos < len(data) and (data[pos] & (1 << bit_idx)):
                    idx |= 1 << plane
            pixels.append(idx)
    return pixels, h


def planar_separate(data: bytes, w: int) -> tuple[list[int], int]:
    """Separate-plane layout: plane0 entire, then plane1 entire, etc."""
    bpr = w // 8
    plane_size_at_h = lambda h: bpr * h
    # h such that bpr*h*4 ≤ len(data); take floor
    h = len(data) // (bpr * 4)
    plane_size = bpr * h
    pixels = []
    for y in range(h):
        for x in range(w):
            byte_idx = x >> 3
            bit_idx = 7 - (x & 7)
            idx = 0
            for plane in range(4):
                pos = plane * plane_size + y * bpr + byte_idx
                if pos < len(data) and (data[pos] & (1 << bit_idx)):
                    idx |= 1 << plane
            pixels.append(idx)
    return pixels, h


def save_png(pixels, w, h, out_path, scale=4):
    img = Image.new("P", (w, h))
    img.putdata(pixels)
    pal = []
    for r, g, b in PAL16:
        pal.extend([r, g, b])
    pal += [0] * (768 - len(pal))
    img.putpalette(pal)
    img.resize((w * scale, h * scale), Image.NEAREST).save(out_path)


def make_contact(folder: Path, suffix: str, thumb_w: int, thumb_h: int):
    pngs = sorted(folder.glob(f"*{suffix}.png"))
    if not pngs:
        return
    cols = 16
    rows = (len(pngs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 30))
    for i, p in enumerate(pngs):
        img = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), Image.NEAREST)
        cx = (i % cols) * thumb_w
        cy = (i // cols) * thumb_h
        sheet.paste(img, (cx, cy))
    sheet_path = folder.parent / f"contact_{suffix.lstrip('_')}.png"
    sheet.save(sheet_path)
    print(f"  contact sheet: {sheet_path}")


def main():
    parts = sorted(PARTS.glob("part_*.bin"))
    print(f"Rendering {len(parts)} parts with 6 hypotheses each")

    hypotheses = [
        # (suffix, render_func, width)
        ("_chunky4_w48_hi", lambda d: chunky_4bpp(d, 48)),
        ("_chunky4_w48_lo", lambda d: chunky_4bpp_lo_first(d, 48)),
        ("_chunky4_w64_hi", lambda d: chunky_4bpp(d, 64)),
        ("_chunky4_w32_hi", lambda d: chunky_4bpp(d, 32)),
        ("_planar_w48",     lambda d: planar_4plane(d, 48)),
        ("_planar_w64_sep", lambda d: planar_separate(d, 64)),
    ]

    for part_path in parts:
        data = part_path.read_bytes()
        for suffix, fn in hypotheses:
            try:
                pixels, h = fn(data)
                w = 48 if "w48" in suffix else 64 if "w64" in suffix else 32
                if h < 4:
                    continue
                save_png(pixels, w, h, OUT / f"{part_path.stem}{suffix}.png")
            except Exception:
                pass

    # 6 contact sheets, one per hypothesis
    for suffix, _ in hypotheses:
        make_contact(OUT, suffix, 48, 80)

    print(f"\n→ {OUT}")
    print("Contact sheets in parent dir.")


if __name__ == "__main__":
    main()
