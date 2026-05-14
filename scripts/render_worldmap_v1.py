#!/usr/bin/env python3
"""Decode + render Worldmap.lzw using JohanLi's pipeline.

Sources (github.com/JohanLi/uncharted-waters-2-research):
  - world_map_blocks.py — block decoder (45×30 blocks of 12×12 large-tile indices)
  - tileset_large.py    — 256 large tiles, each = 2×2 regular tiles (from DATA1.018)
  - tileset_regular.py  — 128 regular tiles, 16×16 / 4bpp / 16 colors (DATA1.011 first half)

Pipeline:
  3 LS11-decompressed Worldmap parts
   → block bitstream decode → (45, 30, 12, 12) large-tile indices
   → reshape to 540×360 large-tile grid
   → expand 2×2 to 1080×720 regular-tile grid
   → blit via regular tileset

Render scales kept conservative to avoid huge PNGs:
  - 1px/tile thumbnail per part (720×1080)
  - 4px/tile detailed per part (2880×4320) — saved as JPEG to stay small

Skips JohanLi's post-processing (coasts, deserts, frigid/temperate, manual fixes).
"""
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
WM_PARTS = REPO / "output" / "lzw_parts" / "Worldmap"
D1_PARTS = REPO / "output" / "lzw_parts" / "Data1"
OUT = REPO / "output" / "worldmap_v1"
OUT.mkdir(parents=True, exist_ok=True)

# Day palette from tileset_regular.py — note 16 entries, JohanLi only defined 14; we fill 2/12 with neutral gray
PALETTE_HEX = {
    0: "000000", 1: "717192", 2: "888888", 3: "0082F3", 4: "D34100",
    5: "A26100", 6: "F3A261", 7: "00B261", 8: "0041D3", 9: "0041C3",
    10: "00A2F3", 11: "007161", 12: "888888", 13: "E3B251", 14: "F3E3D3",
    15: "F3E3D3",
}
PALETTE = np.array(
    [tuple(int(PALETTE_HEX[k][i:i + 2], 16) for i in (0, 2, 4)) for k in range(16)],
    dtype=np.uint8,
)


# ---------- tileset extractors ----------

def extract_regular_tileset() -> np.ndarray:
    """128 tiles × 16×16 × RGB. Encoding identical to Portchip (1024-bit blocks)."""
    raw = (D1_PARTS / "part_0011_32768bytes.bin").read_bytes()
    raw = raw[:len(raw) // 2]  # first half = regular tileset
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    BLOCK_BITS = 1024
    n = len(bits) // BLOCK_BITS  # = 128
    tiles = np.zeros((n, 16, 16, 3), dtype=np.uint8)
    for b in range(n):
        block = bits[b * BLOCK_BITS:(b + 1) * BLOCK_BITS]
        for i in range(256):
            p = (
                (int(block[i]) << 3)
                | (int(block[i + 256]) << 2)
                | (int(block[i + 512]) << 1)
                | int(block[i + 768])
            )
            y, x = divmod(i, 16)
            tiles[b, y, x] = PALETTE[p]
    return tiles


def extract_large_tileset() -> np.ndarray:
    """256 entries; each = 4 regular-tile indices (2×2 arrangement, flat order top-left, top-right, bottom-left, bottom-right)."""
    raw = (D1_PARTS / "part_0018_1024bytes.bin").read_bytes()
    out = np.zeros((256, 4), dtype=np.uint8)
    # First 16 are special: bit pattern of i (4 bits) maps to regular tile 0 or 65
    for i in range(16):
        bits = bin(i)[2:].zfill(4)
        out[i] = [0 if c == "0" else 65 for c in bits]
    # Remaining 240 read 4 bytes each
    cursor = 16 * 4
    for i in range(16, 256):
        for j in range(4):
            v = raw[cursor + j]
            out[i, j] = 0 if v > 128 else v
        cursor += 4
    return out  # shape (256, 4)


# ---------- worldmap block decoder ----------

TEMPLATES_CACHE = {}


def template(number: int) -> np.ndarray:
    if number in TEMPLATES_CACHE:
        return TEMPLATES_CACHE[number].copy()
    t = np.zeros((12, 12), dtype=np.uint8)
    if number == 0:
        t[:, :6] = 15
    elif number == 1:
        t[:, 6:] = 15
    elif number == 2:
        t[:6, :] = 15
    elif number == 3:
        t[6:, :] = 15
    elif number == 4:
        t[:, :] = 15
    TEMPLATES_CACHE[number] = t
    return t.copy()


def decode_part(raw: bytes) -> np.ndarray:
    """Returns (45, 30, 12, 12) array of large-tile indices."""
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    block_bits = bits[2700 * 8:]
    blocks = []
    cursor = 0
    for _ in range(1350):
        is_diff = block_bits[cursor] == 0
        tnum = int(
            "".join(str(int(b)) for b in block_bits[cursor + 5:cursor + 8]), 2
        )
        tile = template(tnum).flatten()
        cursor += 8
        if is_diff:
            corrections = []
            for i in range(144):
                if block_bits[cursor] == 1:
                    corrections.append(i)
                cursor += 1
            for c in corrections:
                v = int("".join(str(int(b)) for b in block_bits[cursor:cursor + 8]), 2)
                tile[c] = v
                cursor += 8
        blocks.append(tile.reshape(12, 12))
    return np.array(blocks).reshape(45, 30, 12, 12)


# ---------- rendering ----------

def expand_to_regular_grid(part: np.ndarray, large_ts: np.ndarray) -> np.ndarray:
    """(45,30,12,12) blocks of large-tile indices → (1080, 720) regular-tile-index grid."""
    # Step 1: flatten blocks to (540, 360) large-tile grid (45 block-rows × 12 = 540, 30 × 12 = 360)
    large_grid = part.transpose(0, 2, 1, 3).reshape(45 * 12, 30 * 12)
    # Step 2: expand each large tile to 2×2 regular tiles
    reg = np.zeros((large_grid.shape[0] * 2, large_grid.shape[1] * 2), dtype=np.uint8)
    for ly in range(large_grid.shape[0]):
        for lx in range(large_grid.shape[1]):
            idx = large_grid[ly, lx]
            tl, tr, bl, br = large_ts[idx]
            reg[ly * 2, lx * 2] = tl
            reg[ly * 2, lx * 2 + 1] = tr
            reg[ly * 2 + 1, lx * 2] = bl
            reg[ly * 2 + 1, lx * 2 + 1] = br
    return reg


def render_thumbnail(grid: np.ndarray, regular_ts: np.ndarray) -> np.ndarray:
    """1 pixel per tile (mean color of tile)."""
    mean_colors = regular_ts.reshape(regular_ts.shape[0], -1, 3).mean(axis=1).astype(np.uint8)
    flat = grid.flatten()
    pixels = mean_colors[np.clip(flat, 0, mean_colors.shape[0] - 1)]
    return pixels.reshape(grid.shape[0], grid.shape[1], 3)


def render_detailed(grid: np.ndarray, regular_ts: np.ndarray, px_per_tile: int = 4) -> np.ndarray:
    """`px_per_tile`-pixels per tile by resizing each tile to px×px then blitting."""
    # Pre-resize each tile
    n = regular_ts.shape[0]
    small_tiles = np.zeros((n, px_per_tile, px_per_tile, 3), dtype=np.uint8)
    for i in range(n):
        small_tiles[i] = np.array(
            Image.fromarray(regular_ts[i], "RGB").resize(
                (px_per_tile, px_per_tile), Image.BILINEAR
            )
        )
    h, w = grid.shape
    out = np.zeros((h * px_per_tile, w * px_per_tile, 3), dtype=np.uint8)
    flat = np.clip(grid, 0, n - 1)
    for y in range(h):
        row = flat[y]
        for x in range(w):
            out[y * px_per_tile:(y + 1) * px_per_tile,
                x * px_per_tile:(x + 1) * px_per_tile] = small_tiles[row[x]]
    return out


def main():
    print("extracting regular tileset (128 tiles, 16×16)...")
    regular_ts = extract_regular_tileset()
    print("extracting large tileset (256 entries × 2×2)...")
    large_ts = extract_large_tileset()
    # large_ts may reference tiles >= 128 in extreme cases; clamp at render time

    parts = sorted(WM_PARTS.glob("*.bin"))
    print(f"decoding {len(parts)} worldmap parts...")

    grids = []
    for pf in parts:
        raw = pf.read_bytes()
        blocks = decode_part(raw)
        grid = expand_to_regular_grid(blocks, large_ts)
        print(f"  {pf.name} → grid {grid.shape}")
        grids.append(grid)

    # JohanLi's combine order: americas + europe_africa + asia (left to right).
    # Our parts: try mapping part0=europe_africa, part1=asia, part2=americas based on
    # JohanLi naming. We'll just render in file order first and combine plainly so
    # the user can identify continents visually.

    # Thumbnails (1px/tile)
    for i, g in enumerate(grids):
        thumb = render_thumbnail(g, regular_ts)
        out = OUT / f"part{i}_thumb.png"
        Image.fromarray(thumb, "RGB").save(out)
        print(f"  → {out.name} ({out.stat().st_size:,} B)  {thumb.shape}")

    # Combined thumbnail (all 3 side by side)
    combined = np.concatenate(grids, axis=1)  # (1080, 2160)
    combined_thumb = render_thumbnail(combined, regular_ts)
    p = OUT.parent / "contact_worldmap_v1.png"
    Image.fromarray(combined_thumb, "RGB").save(p)
    print(f"\n→ combined thumb: {p}  {combined_thumb.shape}  ({p.stat().st_size:,} B)")

    # Detailed per-part (4px/tile = 2880×4320) — save as JPEG to keep size sane, don't Read back
    for i, g in enumerate(grids):
        det = render_detailed(g, regular_ts, px_per_tile=4)
        out = OUT / f"part{i}_4xtile.jpg"
        Image.fromarray(det, "RGB").save(out, quality=85, optimize=True)
        print(f"  → {out.name}  {det.shape}  ({out.stat().st_size:,} B)")


if __name__ == "__main__":
    main()
