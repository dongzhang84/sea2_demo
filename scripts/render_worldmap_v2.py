#!/usr/bin/env python3
"""Worldmap v2 — add JohanLi's post-processing on top of v1.

Pipeline:
  1. decode 3 parts → (1080, 720) regular-tile-index grid (same as v1)
  2. fill_deserts            — expand desert tile 89 into adjacent grass 65
  3. replace_coasts          — replace water (0) with coastal variants via
                               DATA1.010 LUT keyed by 9-bit neighbor pattern
                               (leading '1' + 8 neighbors)
  4. replace_desert_coasts   — swap coastal tiles next to desert for desert-coast
                               variants (+24 offset)
  5. update_frigid_temperate — add +16 to grass in polar rows, +8 in temperate
  6. manual_corrections      — JohanLi's hardcoded fixes for parts 0 and 2

Then render thumbnail (1px/tile) + 4×tile detail JPG.
"""
from pathlib import Path

import numpy as np
from PIL import Image

import render_worldmap_v1 as v1  # reuse tileset extraction + block decoder

REPO = Path(__file__).resolve().parent.parent
D1_PARTS = REPO / "output" / "lzw_parts" / "Data1"
WM_PARTS = REPO / "output" / "lzw_parts" / "Worldmap"
OUT = REPO / "output" / "worldmap_v2"
OUT.mkdir(parents=True, exist_ok=True)

LAND_TILES = set(range(51, 65 + 1)) | {73, 81, 89, 97} | set(range(105, 127 + 1))
DESERT_TILES = {25, 26, 28, 29, 30, 31, 32, 89, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114}

COASTAL_LUT = np.frombuffer((D1_PARTS / "part_0010_512bytes.bin").read_bytes(), dtype=np.uint8)


# ---------- post-processing ----------

def fill_deserts(world_map: np.ndarray) -> np.ndarray:
    rows, cols = world_map.shape
    for c in range(cols):
        for r in range(rows):
            if world_map[r, c] == 89:
                if c + 1 < cols and world_map[r, c + 1] == 65:
                    world_map[r, c + 1] = 89
                if r + 1 < rows and world_map[r + 1, c] == 65:
                    world_map[r + 1, c] = 89
    return world_map


def replace_coasts(world_map: np.ndarray):
    """Vectorized: compute 8-neighbor land mask, look up coastal tile.
    Returns (world_map, list_of_desert_coast_candidates).
    """
    rows, cols = world_map.shape
    land_mask = np.zeros((rows, cols), dtype=bool)
    desert_mask = np.zeros((rows, cols), dtype=bool)
    flat = world_map.ravel()
    for t in LAND_TILES:
        land_mask.ravel()[flat == t] = True
    for t in DESERT_TILES:
        desert_mask.ravel()[flat == t] = True

    # Pad with False borders (out-of-bounds = water).
    padded = np.zeros((rows + 2, cols + 2), dtype=bool)
    padded[1:-1, 1:-1] = land_mask
    desert_padded = np.zeros((rows + 2, cols + 2), dtype=bool)
    desert_padded[1:-1, 1:-1] = desert_mask

    # Neighbor offsets in JohanLi's order:
    #   NW, W, SW, S, SE, E, NE, N
    offs = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    bits = np.zeros((rows, cols), dtype=np.uint16)
    desert_adj = np.zeros((rows, cols), dtype=bool)
    for i, (dr, dc) in enumerate(offs):
        nb = padded[1 + dr:1 + dr + rows, 1 + dc:1 + dc + cols]
        bits |= nb.astype(np.uint16) << (7 - i)
        dnb = desert_padded[1 + dr:1 + dr + rows, 1 + dc:1 + dc + cols]
        desert_adj |= dnb & nb

    # leading "1" bit → OR with 0x100
    lut_idx = bits | 0x100
    water = world_map == 0
    new_tiles = COASTAL_LUT[lut_idx]
    world_map = np.where(water, new_tiles, world_map)

    # Collect coordinates that were water AND have a desert neighbor.
    coords = np.argwhere(water & desert_adj)
    return world_map, [tuple(c) for c in coords]


_ADJ_CHECK = {
    1: [1, 2, 8],
    2: [8],
    3: [6, 7, 8],
    4: [2],
    5: [6],
    6: [2, 3, 4],
    7: [4],
    8: [4, 5, 6],
}
_ADJ_OFFSETS = {
    1: ((-1, -1), {89, 105}),
    2: ((0, -1), {89, 105, 106, 108, 110, 111}),
    3: ((1, -1), {89, 110}),
    4: ((1, 0), {89, 108, 109, 110, 111, 112}),
    5: ((1, 1), {89, 112}),
    6: ((0, 1), {89, 106, 107, 109, 111, 112}),
    7: ((-1, 1), {89, 107}),
    8: ((-1, 0), {89, 105, 106, 107, 108, 109}),
}


def replace_desert_coasts(world_map: np.ndarray, candidates: list) -> np.ndarray:
    rows, cols = world_map.shape
    for r, c in candidates:
        t = int(world_map[r, c])
        if t not in _ADJ_CHECK:
            continue
        ok = True
        for x in _ADJ_CHECK[t]:
            (dr, dc), allowed = _ADJ_OFFSETS[x]
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                ok = False
                break
            if int(world_map[nr, nc]) not in allowed:
                ok = False
                break
        if ok and world_map[r, c] != 0:
            world_map[r, c] = world_map[r, c] + 24
    return world_map


def update_frigid_temperate(world_map: np.ndarray) -> np.ndarray:
    rows, _ = world_map.shape
    mask = np.zeros_like(world_map, dtype=bool)
    for t in list(range(1, 8 + 1)) + list(range(65, 72 + 1)):
        mask |= world_map == t
    row_idx = np.arange(rows)[:, None]
    frigid_rows = (row_idx < 24) | (row_idx >= rows - 24)
    temperate_rows = ((row_idx < 24 * 14) | (row_idx >= 24 * 31)) & ~frigid_rows
    world_map = np.where(mask & frigid_rows, world_map + 16, world_map)
    world_map = np.where(mask & temperate_rows, world_map + 8, world_map)
    return world_map


def manual_corrections(world_map: np.ndarray, part_idx: int) -> np.ndarray:
    if part_idx == 0:
        world_map[444, 366] = 28
        world_map[445, 366] = 28
        world_map[489, 415] = 27
        world_map[1055, 266] = 23
        world_map[1055, 267] = 23
    if part_idx == 2:
        world_map[890, 134] = 26
        world_map[890, 135] = 26
        world_map[1056, 417] = 13
        world_map[1061, 435] = 12
    return world_map


# ---------- main ----------

def main():
    print("extracting regular tileset...")
    regular_ts = v1.extract_regular_tileset()
    print("extracting large tileset...")
    large_ts = v1.extract_large_tileset()

    parts = sorted(WM_PARTS.glob("*.bin"))
    grids = []
    for pi, pf in enumerate(parts):
        raw = pf.read_bytes()
        blocks = v1.decode_part(raw)
        g = v1.expand_to_regular_grid(blocks, large_ts).astype(np.int32)

        print(f"  {pf.name} → grid {g.shape}, post-processing...")
        g = fill_deserts(g)
        g, candidates = replace_coasts(g)
        g = replace_desert_coasts(g, candidates)
        g = update_frigid_temperate(g)
        g = manual_corrections(g, pi)
        grids.append(g)

    # Thumbnail (1px/tile)
    for i, g in enumerate(grids):
        thumb = v1.render_thumbnail(g, regular_ts)
        p = OUT / f"part{i}_thumb.png"
        Image.fromarray(thumb, "RGB").save(p)
        print(f"  → {p.name} ({p.stat().st_size:,} B)  {thumb.shape}")

    combined = np.concatenate(grids, axis=1)
    combined_thumb = v1.render_thumbnail(combined, regular_ts)
    p = OUT.parent / "contact_worldmap_v2.png"
    Image.fromarray(combined_thumb, "RGB").save(p)
    print(f"\n→ combined thumb: {p}  {combined_thumb.shape}  ({p.stat().st_size:,} B)")

    for i, g in enumerate(grids):
        det = v1.render_detailed(g, regular_ts, px_per_tile=4)
        p = OUT / f"part{i}_4xtile.jpg"
        Image.fromarray(det, "RGB").save(p, quality=85, optimize=True)
        print(f"  → {p.name}  {det.shape}  ({p.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
