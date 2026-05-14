#!/usr/bin/env python3
"""Render each decoded variant as grayscale images at multiple widths.
The 'right' decoder produces output with visible image-like structure.

Specifically targets the first ~2,560 bytes of each Kao_*.bin (one portrait).
"""
from pathlib import Path
from PIL import Image

DECODED_DIR = Path("/Users/dong/Projects/sea2_demo/output/decompressed")
OUT_DIR = Path("/Users/dong/Projects/sea2_demo/output/visualize")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save_gray(data: bytes, width: int, out_path: Path, scale: int = 3) -> None:
    height = (len(data) + width - 1) // width
    img = Image.new("L", (width, height))
    padded = data + b"\x00" * (width * height - len(data))
    img.putdata(list(padded))
    img = img.resize((width * scale, height * scale), Image.NEAREST)
    img.save(out_path)


def main():
    files = sorted(DECODED_DIR.glob("Kao_*.bin"))
    print(f"Visualizing {len(files)} Kao decoded variants")
    for f in files:
        data = f.read_bytes()
        variant = f.stem.replace("Kao_", "")

        # Whole-file at width 320 (typical row stride for image archive)
        save_gray(data[:80000], 320, OUT_DIR / f"Kao_{variant}_FULL_w320.png", scale=1)

        # First ~5KB rendered at common portrait widths
        sample = data[:8000]
        for w in [32, 40, 48, 64, 80, 128, 160]:
            save_gray(sample, w, OUT_DIR / f"Kao_{variant}_sample_w{w:03d}.png")

        # Histogram for variety check
        hist = [0] * 256
        for b in data[:50000]:
            hist[b] += 1
        top = sorted(enumerate(hist), key=lambda kv: -kv[1])[:5]
        print(f"  {variant}: top 5 bytes = " + ", ".join(f"0x{b:02x}({c})" for b, c in top))

    # Also Char and Data1
    for stem in ("Char", "Data1"):
        files = sorted(DECODED_DIR.glob(f"{stem}_*.bin"))
        print(f"\nVisualizing {len(files)} {stem} variants")
        for f in files:
            data = f.read_bytes()[:30000]
            variant = f.stem.replace(f"{stem}_", "")
            # Char is likely 16x16 glyphs = 32 bytes each, render at common widths
            for w in [16, 32, 64, 128, 256]:
                save_gray(data, w, OUT_DIR / f"{stem}_{variant}_w{w:03d}.png")

    print(f"\n→ {OUT_DIR}")
    print("Look for: faces, glyph grids, or any non-noise structure.")


if __name__ == "__main__":
    main()
