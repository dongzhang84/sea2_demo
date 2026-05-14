#!/usr/bin/env python3
"""Extract ship sprites + ship stats from Data1.lzw.

Based on JohanLi's tileset_ship.py and ships/extract_metadata.py.

Output:
  output/ships/ship_NN.png       — 32 sprites (32×32, transparent BG)
  output/ships/contact.png       — overview of all 32
  output/game_data/ships.json    — 25 ships × full stat table
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
OUT_SPRITES = REPO / "output" / "ships"
OUT_SPRITES.mkdir(parents=True, exist_ok=True)
OUT_DATA = REPO / "output" / "game_data"

# 8-color palette with transparency for ships
PAL_HEX = ["000000", "00a261", "d34100", "f3a261",
           "0041d3", "00a2f3", "d361a2", "f3e3d3"]
PAL_RGBA = np.zeros((9, 4), dtype=np.uint8)
for i, h in enumerate(PAL_HEX):
    PAL_RGBA[i] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
# color index 8 = transparent
PAL_RGBA[8] = (0, 0, 0, 0)


def extract_sprites():
    raw = (REPO / "output" / "lzw_parts" / "Data1" / "part_0011_32768bytes.bin").read_bytes()
    ship_half = raw[len(raw) // 2:]  # second half = ship tileset
    bits = np.unpackbits(np.frombuffer(ship_half, dtype=np.uint8))
    width = height = 32
    bpp = 4
    block_bits = 64  # 64 bits = 16 pixels per block (4bpp planar)
    n_sprites = len(bits) // (width * height * bpp)
    print(f"  ship data: {len(ship_half)} bytes → {n_sprites} sprites ({width}×{height})")

    pixel_blocks = np.split(bits, len(bits) // block_bits)
    block_increment = block_bits // bpp  # 16
    flat_pixels = []
    for block in pixel_blocks:
        for i in range(block_increment):
            pixel_bits = ''.join(map(str, block[i::block_increment]))
            pixel_value = int(pixel_bits, 2)
            flat_pixels.append(pixel_value)
    arr = np.array(flat_pixels, dtype=np.uint8).reshape(n_sprites, height, width)

    sprites = []
    for i in range(n_sprites):
        rgba = PAL_RGBA[arr[i]]
        img = Image.fromarray(rgba, "RGBA")
        img.save(OUT_SPRITES / f"ship_{i:02d}.png")
        sprites.append(img)
    print(f"  saved {n_sprites} ship sprites")

    # Contact sheet: 8 cols × N rows, 4× scale
    SCALE = 4
    cols = 8
    rows = (n_sprites + cols - 1) // cols
    GAP = 4
    sheet = Image.new("RGBA", (cols * (width * SCALE + GAP), rows * (height * SCALE + GAP)),
                       (40, 40, 60, 255))
    for i, sp in enumerate(sprites):
        r, c = divmod(i, cols)
        big = sp.resize((width * SCALE, height * SCALE), Image.NEAREST)
        sheet.paste(big, (c * (width * SCALE + GAP), r * (height * SCALE + GAP)), big)
    sheet_path = REPO / "output" / "contact_ships.png"
    sheet.save(sheet_path)
    print(f'  contact: {sheet_path}  ({sheet_path.stat().st_size:,} B)')
    return n_sprites


def extract_stats():
    raw = (REPO / "output" / "lzw_parts" / "Data1" / "part_0015_32117bytes.bin").read_bytes()
    ships = {}

    # TC-version offsets (found by pattern search, NOT JohanLi's English-version offsets):
    # Stats table at 0x5184 (20868), names table assumed 600 bytes before at 0x4F2C (20268)
    STATS_OFFSET = 0x5184
    NAME_OFFSET = STATS_OFFSET - 24 * 25  # = 0x4F2C = 20268

    # Section 1: name + used_guns + used_crew (24 bytes each, 25 ships)
    cursor = NAME_OFFSET
    for i in range(1, 26):
        rec = raw[cursor:cursor + 24]
        name_bytes = rec[:16]
        name_clean = name_bytes.rstrip(b'\x00 ')
        ships[i] = {
            'id': i,
            'name_hex': name_clean.hex(),
            'name_ascii_attempt': name_clean.decode('ascii', errors='replace'),
            'used_guns': rec[19],
            'used_crew': int.from_bytes(rec[20:22], 'little'),
        }
        cursor += 24

    # Section 2: detailed stats (12 bytes each)
    cursor = STATS_OFFSET
    for i in range(1, 26):
        rec = raw[cursor:cursor + 12]
        ships[i]['industry_requirement'] = rec[0] * 10
        ships[i]['durability'] = rec[1]
        ships[i]['tacking'] = rec[2]
        ships[i]['power'] = rec[3]
        ships[i]['maximum_crew'] = rec[4] * 10
        ships[i]['minimum_crew'] = rec[5]
        ships[i]['capacity_tons'] = int.from_bytes(rec[6:8], 'little')
        ships[i]['maximum_guns'] = rec[8]
        ships[i]['sail_type'] = rec[9] + 1
        ships[i]['base_price'] = int.from_bytes(rec[10:12], 'little') * 10
        cursor += 12

    # Save JSON
    OUT_DATA.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DATA / 'ships.json'
    out_path.write_text(json.dumps({
        'count': len(ships),
        'note': 'Extracted from Data1.lzw part_0015 at offsets 19388 & 19988 (per JohanLi). '
                'Names are in KOEI custom CJK encoding — raw hex preserved.',
        'ships': list(ships.values()),
    }, indent=2, ensure_ascii=False))
    print(f'  → {out_path}  ({len(ships)} ships)')

    # Print first 5 as sanity check
    print('  first 5 ships:')
    for i in [1, 2, 3, 4, 5]:
        s = ships[i]
        print(f'    #{i:2}  name_hex={s["name_hex"][:24]:<24}  '
              f'guns {s["maximum_guns"]:>3}  crew {s["maximum_crew"]:>3}  '
              f'capacity {s["capacity_tons"]:>4}  price {s["base_price"]:>6}')
    return len(ships)


def main():
    print('=== Ship sprites ===')
    n_sprites = extract_sprites()
    print(f'\n=== Ship stats ===')
    n_ships = extract_stats()
    print(f'\nDone: {n_sprites} sprites + {n_ships} stat records')


if __name__ == '__main__':
    main()
