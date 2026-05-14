#!/usr/bin/env python3
"""Render the 128 "discoveries + items" sprites from Kao.lzw's trailing parts.

Format (verified 2026-05-14):
  - 864 bytes per part = 288 blocks of 24 bits = 2304 pixels = 48×48
  - 3-plane 8-color, identical encoding to the 80×64 portraits in render_kao_v4.py
  - Same 8-color palette (JohanLi)

Content: animals, landmarks, weapons, armor, food, treasure — i.e. the
"discoveries" the player collects in Uncharted Waters II / 大航海時代II.
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PARTS = REPO / "output" / "kao_parts"
OUT = REPO / "output" / "disc_png_v1"
OUT.mkdir(parents=True, exist_ok=True)

W, H, PLANES = 48, 48, 3
BLOCK_BITS = 8 * PLANES  # 24

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


def decode_sprite(raw_bytes: bytes) -> np.ndarray:
    bits = np.unpackbits(np.frombuffer(raw_bytes, dtype=np.uint8))
    pixels = []
    pointer = 0
    while pointer + BLOCK_BITS <= len(bits):
        for j in range(8):
            idx = (
                (int(bits[pointer + j]) << 2)
                | (int(bits[pointer + j + 8]) << 1)
                | int(bits[pointer + j + 16])
            )
            pixels.append(COLOR_MAP[idx])
        pointer += BLOCK_BITS
    arr = np.array(pixels, dtype=np.uint8)
    if arr.size != W * H * 3:
        return None
    return arr.reshape(H, W, 3)


def main():
    parts = sorted(PARTS.glob("*_864bytes.bin"))
    print(f"rendering {len(parts)} sprites at {W}×{H} / 3-plane / 8-color")

    images = []
    for i, p in enumerate(parts):
        arr = decode_sprite(p.read_bytes())
        if arr is None:
            print(f"  skip {p.name} (size mismatch)")
            continue
        img = Image.fromarray(arr, "RGB")
        img.resize((W * 3, H * 3), Image.NEAREST).save(OUT / f"{i:03d}.png")
        images.append(img)

    cols, thumb_w, thumb_h = 16, W * 2, H * 2
    rows = (len(images) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), (20, 20, 30))
    for i, img in enumerate(images):
        sheet.paste(
            img.resize((thumb_w, thumb_h), Image.NEAREST),
            ((i % cols) * thumb_w, (i // cols) * thumb_h),
        )
    sheet_path = OUT.parent / "contact_disc_v1.png"
    sheet.save(sheet_path)
    print(f"\n→ {OUT}")
    print(f"→ contact: {sheet_path}")


if __name__ == "__main__":
    main()
