#!/usr/bin/env python3
"""高清世界地图渲染 —— 给游戏的滚动镜头用。

复用 worldmap v2 的解码 + 后处理管线，把 3 个 part 拼成完整世界图，
按 8 像素/tile 渲染（原生是 16px/tile，8 折中：清晰且文件不爆）。

输出：game/assets/world/worldmap_hi.jpg
完整世界 = 2160×1080 tile → 8px/tile → 17280×8640 像素。
"""
from pathlib import Path

import numpy as np
from PIL import Image

import render_worldmap_v1 as v1
import render_worldmap_v2 as v2

REPO = Path(__file__).resolve().parent.parent
WM_PARTS = REPO / "output" / "lzw_parts" / "Worldmap"
PX_PER_TILE = 7


def main():
    print("提取 tileset...")
    regular_ts = v1.extract_regular_tileset()
    large_ts = v1.extract_large_tileset()

    grids = []
    for pi, pf in enumerate(sorted(WM_PARTS.glob("*.bin"))):
        blocks = v1.decode_part(pf.read_bytes())
        g = v1.expand_to_regular_grid(blocks, large_ts).astype(np.int32)
        g = v2.fill_deserts(g)
        g, cand = v2.replace_coasts(g)
        g = v2.replace_desert_coasts(g, cand)
        g = v2.update_frigid_temperate(g)
        g = v2.manual_corrections(g, pi)
        grids.append(g)
        print(f"  part{pi} grid {g.shape} 后处理完")

    combined = np.concatenate(grids, axis=1)
    print(f"合并网格 {combined.shape} (行,列) → 渲染 {PX_PER_TILE}px/tile ...")
    det = v1.render_detailed(combined, regular_ts, px_per_tile=PX_PER_TILE)
    print(f"渲染完成 {det.shape}")

    # 世界地图只有 16 色 → 量化成调色板 PNG, 体积远小于 JPEG, 且无损
    im = Image.fromarray(det, "RGB").quantize(colors=16, method=Image.MEDIANCUT)
    out = REPO / "game" / "assets" / "world" / "worldmap_hi.png"
    im.save(out, optimize=True)
    print(f"→ {out}  ({out.stat().st_size:,} 字节)")


if __name__ == "__main__":
    main()
