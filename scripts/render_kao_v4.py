#!/usr/bin/env python3
"""v4 — JohanLi's actual 大航海II portrait format.

Source: github.com/JohanLi/uncharted-waters-2-research/portraits-items-discoveries/portraits.py

Format per 1920-byte part:
  - 80×64 pixels, 8 colors
  - Unpack to 15,360 bits
  - For each 8-pixel block: pointer advances by 24 bits (3 bytes)
    Pixel j (0..7) color index = 3 bits at (pointer+j, pointer+j+8, pointer+j+16)
  - 640 blocks total → 5,120 pixels → reshape to (80, 64)
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PARTS = REPO / "output" / "kao_parts"
OUT = REPO / "output" / "kao_png_v4"
OUT.mkdir(parents=True, exist_ok=True)

COLOR_MAP = {
    0: (0x00, 0x00, 0x00),
    1: (0x00, 0xA0, 0x60),
    2: (0xD0, 0x40, 0x00),
    3: (0xF0, 0xA0, 0x60),
    4: (0x00, 0x40, 0xD0),
    5: (0x00, 0xA0, 0xF0),
    6: (0xD0, 0x60, 0xA0),
    7: (0xF0, 0xE0, 0xD0),
}


def decode_portrait(raw_bytes: bytes) -> np.ndarray:
    bits = np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))
    pixels = []
    pointer = 0
    while pointer + 24 <= len(bits):
        for j in range(8):
            idx = (int(bits[pointer + j]) << 2) | (int(bits[pointer + j + 8]) << 1) | int(bits[pointer + j + 16])
            pixels.append(COLOR_MAP[idx])
        pointer += 24
    arr = np.array(pixels, dtype=np.uint8)
    if arr.size != 80 * 64 * 3:
        return None
    return arr.reshape(80, 64, 3)


def main():
    parts = sorted(PARTS.glob("*_1920bytes.bin"))
    print(f"v4: rendering {len(parts)} full-size parts as 80×64 8-color portraits")

    images = []
    for i, p in enumerate(parts):
        arr = decode_portrait(p.read_bytes())
        if arr is None:
            print(f"  skip {p.name} (size mismatch)")
            continue
        img = Image.fromarray(arr, "RGB")
        img.resize((64 * 3, 80 * 3), Image.NEAREST).save(OUT / f"{i:03d}.png")
        images.append(img)

    # Contact sheet: 16 cols × 8 rows
    cols, thumb_w, thumb_h = 16, 64 * 2, 80 * 2
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 30))
    for i, img in enumerate(images):
        sheet.paste(img.resize((thumb_w, thumb_h), Image.NEAREST), ((i % cols) * thumb_w, (i // cols) * thumb_h))
    sheet_path = OUT.parent / "contact_kao_v4.png"
    sheet.save(sheet_path)
    print(f"\n→ {OUT}")
    print(f"→ contact: {sheet_path}")


if __name__ == "__main__":
    main()
