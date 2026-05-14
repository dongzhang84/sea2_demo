#!/usr/bin/env python3
"""Render Char.lzw — walking sprites for characters on world map.

(Not a font, despite the name. JohanLi's `portraits-items-discoveries/char.py`.)

Each 32×32 frame split into 4 quadrants of 16×16. Each quadrant has 5 bit-planes:
  - 4 color planes (4 bpp = 16 colors)
  - 1 transparency plane (1 = transparent)
Plane stride = 16×16 = 256 bits = 32 bytes. 5 planes × 32 bytes = 160 bytes/quadrant.
4 quadrants × 160 = 640 bytes/frame.

Files:
  part_0000..part_0005 = 5120 bytes = 8 frames each (chars 0-5)
  part_0006            = 15360 bytes = 24 frames (char 6, more animations)
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
PARTS = REPO / "output" / "lzw_parts" / "Char"
OUT = REPO / "output" / "char_v2"
OUT.mkdir(parents=True, exist_ok=True)

# JohanLi's color_map for char sprites (uses indices 0, 2, 4, 6, 8, 10, 12, 14)
COLOR_HEX = {
    0: "000000", 2: "00A261", 4: "D34100", 6: "F3A261",
    8: "0041D3", 10: "00A2F3", 12: "D361A2", 14: "F3E3D3",
}
PAL_RGBA = np.zeros((16, 4), dtype=np.uint8)
for k in range(16):
    h = COLOR_HEX.get(k, "808080")
    PAL_RGBA[k] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

QUAD_BITS_PER_PLANE = 16 * 16
QUAD_PLANE_BYTES = QUAD_BITS_PER_PLANE // 8  # 32
QUAD_BYTES = 5 * QUAD_PLANE_BYTES             # 160
FRAME_BYTES = 4 * QUAD_BYTES                   # 640


def render_frame(raw: bytes) -> np.ndarray:
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    img = np.zeros((32, 32, 4), dtype=np.uint8)
    pointer = 0
    # quadrant order: top-left, top-right, bottom-left, bottom-right
    quad_offsets = [(0, 0), (0, 16), (16, 0), (16, 16)]
    for qy, qx in quad_offsets:
        for j in range(QUAD_BITS_PER_PLANE):
            p0 = int(bits[pointer + j])
            p1 = int(bits[pointer + j + 1 * QUAD_BITS_PER_PLANE])
            p2 = int(bits[pointer + j + 2 * QUAD_BITS_PER_PLANE])
            p3 = int(bits[pointer + j + 3 * QUAD_BITS_PER_PLANE])
            alpha_bit = int(bits[pointer + j + 4 * QUAD_BITS_PER_PLANE])
            idx = (p0 << 3) | (p1 << 2) | (p2 << 1) | p3
            row, col = divmod(j, 16)
            if alpha_bit == 1:
                img[qy + row, qx + col] = (0, 0, 0, 0)
            else:
                img[qy + row, qx + col] = PAL_RGBA[idx]
        pointer += 5 * QUAD_BITS_PER_PLANE
    return img


def main():
    parts = sorted(PARTS.glob("*.bin"))
    print(f"Char.lzw: {len(parts)} parts")

    all_frames = []
    for ci, pf in enumerate(parts):
        raw = pf.read_bytes()
        n_frames = len(raw) // FRAME_BYTES
        char_dir = OUT / f"char{ci}"
        char_dir.mkdir(exist_ok=True)
        for fi in range(n_frames):
            frame_raw = raw[fi * FRAME_BYTES:(fi + 1) * FRAME_BYTES]
            arr = render_frame(frame_raw)
            Image.fromarray(arr, "RGBA").save(char_dir / f"frame{fi:02d}.png")
            all_frames.append((ci, fi, arr))
        print(f"  char {ci}: {n_frames} frames → {char_dir.name}/")

    # Contact sheet: 8 cols. char 0-5 take 1 row each (8 frames). char 6's 24
    # frames wrap onto 3 rows. Total 9 rows × 8 cols.
    CELL = 64
    GAP = 4
    COLS = 8
    char_count = max(c for c, _, _ in all_frames) + 1
    placements = []
    cur_row = 0
    for ci in range(char_count):
        cf = [(c, f, a) for c, f, a in all_frames if c == ci]
        for f_idx, (_, _, arr) in enumerate(cf):
            r = cur_row + f_idx // COLS
            col = f_idx % COLS
            placements.append((r, col, arr))
        cur_row += (len(cf) + COLS - 1) // COLS
    rows = cur_row
    sheet = Image.new("RGBA", (COLS * (CELL + GAP), rows * (CELL + GAP)),
                       (40, 40, 60, 255))
    for r, c, arr in placements:
        im = Image.fromarray(arr, "RGBA").resize((CELL, CELL), Image.NEAREST)
        sheet.paste(im, (c * (CELL + GAP) + 2, r * (CELL + GAP) + 2), im)
    out = REPO / "output" / "contact_char_v2.png"
    sheet.save(out)
    print(f"\n→ {out} ({out.stat().st_size:,} B)  {len(all_frames)} frames, {rows} rows")


if __name__ == "__main__":
    main()
