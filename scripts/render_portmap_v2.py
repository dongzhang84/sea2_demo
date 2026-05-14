#!/usr/bin/env python3
"""Render Portmap.lzw with real Portchip tile graphics.

Portmap byte values range 0..239, matching the 240 tiles in one Portchip part.
For a first pass we use Portchip part 0 (likely a standard atlas).
"""
from pathlib import Path

import numpy as np
from PIL import Image

import render_portchip_v2 as pc

REPO = Path(__file__).resolve().parent.parent
PORTMAP = REPO / "output" / "lzw_parts" / "Portmap"
PORTCHIP = REPO / "output" / "lzw_parts" / "Portchip"
CHIP_NO = Path("/Users/dong/Projects/Koukai2/Chip_no.dat")
OUT = REPO / "output" / "portmap_v2"
OUT.mkdir(parents=True, exist_ok=True)

W = H = 96  # tile-cells per port map
T = 16     # tile size


def main():
    # Load the 7 chip atlases
    chip_parts = sorted([p for p in PORTCHIP.glob("*.bin") if p.stat().st_size == 30720])
    atlases = [pc.decode_part(p.read_bytes()) for p in chip_parts]
    print(f"loaded {len(atlases)} Portchip atlases ({atlases[0].shape[0]} tiles each)")

    port_files = sorted(PORTMAP.glob("*.bin"))

    # Chip_no.dat: per-port atlas index (100 bytes, 0..6). Extend with atlas 0 if
    # we have more ports than entries (101 ports vs 100 bytes — last port falls
    # back to atlas 0).
    chip_no = list(CHIP_NO.read_bytes())
    while len(chip_no) < len(port_files):
        chip_no.append(0)
    print(f"chip_no map: {len(chip_no)} entries, values used: {sorted(set(chip_no))}")

    rendered = []
    for pi, pf in enumerate(port_files):
        atlas = atlases[chip_no[pi]]
        idx = np.frombuffer(pf.read_bytes(), dtype=np.uint8).reshape(H, W)
        img = np.zeros((H * T, W * T, 3), dtype=np.uint8)
        for y in range(H):
            for x in range(W):
                tile_id = idx[y, x]
                if tile_id < atlas.shape[0]:
                    img[y * T:(y + 1) * T, x * T:(x + 1) * T] = atlas[tile_id]
        rendered.append(img)

    # Save individual PNGs at 1× (already 1536×1536) — but cap size by using 0.5× downscale for contact
    for i, img in enumerate(rendered):
        Image.fromarray(img, "RGB").save(OUT / f"{i:03d}.png")

    # Full contact sheet: 10 cols × ~11 rows, 1px-per-cell thumbs
    cols = 10
    rows = (len(rendered) + cols - 1) // cols
    THUMB = 192
    sheet = Image.new("RGB", (cols * THUMB, rows * THUMB), (20, 20, 30))
    for i, img in enumerate(rendered):
        thumb = Image.fromarray(img, "RGB").resize((THUMB, THUMB), Image.BILINEAR)
        sheet.paste(thumb, ((i % cols) * THUMB, (i // cols) * THUMB))
    out_path = OUT.parent / "contact_portmap_v2.png"
    sheet.save(out_path)
    print(f"\n→ {OUT}")
    print(f"→ contact: {out_path}  ({out_path.stat().st_size:,} B)")

    # 2×2 sample contact for ports 000-003
    LARGE = 768
    sheet2 = Image.new("RGB", (LARGE * 2, LARGE * 2), (20, 20, 30))
    for i in range(4):
        big = Image.fromarray(rendered[i], "RGB").resize((LARGE, LARGE), Image.BILINEAR)
        sheet2.paste(big, ((i % 2) * LARGE, (i // 2) * LARGE))
    out2 = OUT.parent / "contact_portmap_v2_2x2.png"
    sheet2.save(out2)
    print(f"→ 2x2 (ports 0-3): {out2}  ({out2.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
