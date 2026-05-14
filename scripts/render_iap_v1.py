#!/usr/bin/env python3
"""Render Iap1-6.lzw — player/character duel sprites.

Format (from JohanLi's dueling/extract_iap.py):
  Each part starts with a metadata table. Each entry is 8 bytes:
    x (u8), y (u8), columns (u8), rows (u8), start_address (u32 big-endian)
  Read entries until `bytes_read >= first_entry.start_address`.
  Each sprite's bitmap is columns*4*rows bytes at start_address.
  Bitmap = 4-plane interleaved 8-pixel blocks (32 bits per 8-pixel chunk).
  Color index = bits[p+j], bits[p+j+8], bits[p+j+16], bits[p+j+24] (MSB first).

Color map (11 entries, index 1 = transparent):
  0=#000000  1=transparent  2=#00A261  4=#D34100  6=#F3A200
  8=#0041D3  9=#0040D0  10=#00A2F3  12=#F341C3  13=#F040C0  14=#F3E3D3
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "output" / "iap_v1"
OUT.mkdir(parents=True, exist_ok=True)

COLOR_MAP = {
    0: "000000", 1: None, 2: "00A261", 4: "D34100", 6: "F3A200",
    8: "0041D3", 9: "0040D0", 10: "00A2F3", 12: "F341C3", 13: "F040C0", 14: "F3E3D3",
}
PALETTE_RGBA = np.zeros((16, 4), dtype=np.uint8)
for k in range(16):
    hexv = COLOR_MAP.get(k)
    if hexv is None:
        PALETTE_RGBA[k] = (0, 0, 0, 0)
    else:
        PALETTE_RGBA[k] = (
            int(hexv[0:2], 16), int(hexv[2:4], 16), int(hexv[4:6], 16), 255,
        )


def parse_part(raw: bytes):
    """Return list of (metadata_dict, sprite_rgba_array)."""
    sprites = []
    metas = []
    cursor = 0
    while True:
        x = raw[cursor]
        y = raw[cursor + 1]
        cols = raw[cursor + 2]
        rows = raw[cursor + 3]
        start = int.from_bytes(raw[cursor + 4:cursor + 8], "big")
        metas.append({"x": x, "y": y, "cols": cols, "rows": rows, "start": start})
        cursor += 8
        if cursor >= metas[0]["start"]:
            break

    arr = np.frombuffer(raw, dtype=np.uint8)
    for m in metas:
        s, c, r = m["start"], m["cols"], m["rows"]
        n_bytes = c * 4 * r
        chunk = arr[s:s + n_bytes]
        if len(chunk) != n_bytes:
            continue
        bits = np.unpackbits(chunk)
        # 8-pixel rows of width c*8, total r rows. Each 8-pixel block = 32 bits.
        # Layout per block: plane0 bits (8), plane1 (8), plane2 (8), plane3 (8).
        pixels = np.zeros((r, c * 8), dtype=np.uint8)
        # number of 8-pixel blocks total = c * r (each row has c blocks)
        # bits layout: blocks consecutive in raster order
        pointer = 0
        for row in range(r):
            for bx in range(c):
                for j in range(8):
                    p0 = int(bits[pointer + j])
                    p1 = int(bits[pointer + j + 8])
                    p2 = int(bits[pointer + j + 16])
                    p3 = int(bits[pointer + j + 24])
                    pixels[row, bx * 8 + j] = (p0 << 3) | (p1 << 2) | (p2 << 1) | p3
                pointer += 32
        rgba = PALETTE_RGBA[pixels]
        sprites.append((m, rgba))
    return sprites


def render_set(name: str):
    in_dir = REPO / "output" / "lzw_parts" / name
    if not in_dir.exists():
        return
    out_dir = OUT / name
    out_dir.mkdir(parents=True, exist_ok=True)

    parts = sorted(in_dir.glob("*.bin"))
    print(f"{name}: {len(parts)} parts")

    all_imgs = []
    for pi, pf in enumerate(parts):
        sprites = parse_part(pf.read_bytes())
        for si, (m, rgba) in enumerate(sprites):
            img = Image.fromarray(rgba, "RGBA")
            img.save(out_dir / f"p{pi:02d}_s{si:02d}.png")
            all_imgs.append(img)

    if not all_imgs:
        return

    max_w = max(im.size[0] for im in all_imgs)
    max_h = max(im.size[1] for im in all_imgs)
    cell_w, cell_h = max_w + 4, max_h + 4
    cols = 12
    rows = (len(all_imgs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (40, 40, 60, 255))
    for i, im in enumerate(all_imgs):
        sheet.paste(im, ((i % cols) * cell_w + 2, (i // cols) * cell_h + 2), im)
    p = REPO / "output" / f"contact_{name.lower()}_v1.png"
    sheet.save(p)
    print(f"  → {p.name} ({p.stat().st_size:,} B)  {len(all_imgs)} sprites")


def main():
    for fi in range(1, 7):
        render_set(f"Iap{fi}")
    render_set("Iae1")


if __name__ == "__main__":
    main()
