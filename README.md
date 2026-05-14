# sea2_demo — 大航海時代II 资源逆向

KOEI《大航海時代II》(Uncharted Waters II, 1993, PC-9801) 的资源文件逆向。

源文件不在 git 里（本地路径 `/Users/dong/Projects/Koukai2/`）。

## 当前进度

| 资源 | 状态 | 输出 |
|---|---|---|
| `Kao.lzw` — 128 张头像 | ✅ | ![](output/contact_kao_v4.png) |
| `Kao.lzw` — 128 个 48×48 发现物/道具 | ✅ | `output/contact_disc_v1.png` |
| `Portchip.lzw` — 7 套港口 tile atlas | ✅ | `output/portchip_v2/` |
| `Portmap.lzw` — 101 个港口地图 | ✅ | `output/contact_portmap_v2.png` |
| `Worldmap.lzw` — 3 张世界地图（含沙漠/海岸/极地后处理）| ✅ | `output/contact_worldmap_v2.png` |
| `Char.lzw` — 字体 | 🟥 卡住 | — |
| `Iap1-6.lzw` `Iae1.lzw` — 决斗界面 | ⬜ | — |
| `Opgraph.lzw` — 开场动画 | ⬜ | — |
| `Data1.lzw` 剩余 part — 船舶/UI/动画 | ⬜ | — |
| 数据表（`.dat`）| ⬜ | — |

完整计划见 **[ROADMAP.md](ROADMAP.md)**。技术细节见 **[CLAUDE.md](CLAUDE.md)**。

## 跑一遍

```bash
pip install Pillow numpy

# 1. 解压所有 .lzw → output/lzw_parts/{Kao,Portchip,...}/
python3 scripts/inventory_lzw.py

# 2. 渲染所有解出来的资源
python3 scripts/render_kao_v4.py        # 128 头像
python3 scripts/render_disc_v1.py       # 128 发现物
python3 scripts/render_portchip_v2.py   # 7 套 atlas
python3 scripts/render_portmap_v2.py    # 101 港口
python3 scripts/render_worldmap_v2.py   # 3 张世界图（含后处理）
```

## 目录

```
scripts/
  ls11_decode.py              — LS10/LS11/Ls12 解压器
  inventory_lzw.py            — 批量解压所有 .lzw
  render_kao_v4.py            — 80×64 / 3-plane / 8 色头像
  render_disc_v1.py           — 48×48 / 3-plane / 8 色发现物
  render_portchip_v2.py       — 16×16 / 4bpp / 16 色港口 atlas
  render_portmap_v2.py        — Portmap × Portchip × Chip_no.dat
  render_worldmap_v1.py       — 块解码 + tile 拼图（基础版）
  render_worldmap_v2.py       — v1 + 沙漠/海岸/极地后处理
  experiments/                — 失败的尝试，保留作历史记录

output/
  contact_*.png               — 各资源的总览图
  kao_png_v4/ disc_png_v1/    — 单图（128 张）
  portchip_v2/ portmap_v2/    — 全部 atlas / 港口图
  worldmap_v2/                — 世界图缩略 PNG + 4×tile JPG
  lzw_parts/                  — LS11 解压出的原始 part（gitignore）
```

## 关键参考

- [JohanLi/uncharted-waters-2-research](https://github.com/JohanLi/uncharted-waters-2-research) — 救命级参考：tile 编码、large tileset、worldmap 后处理、决斗 UI
- [tzengyuxio/kaodata](https://github.com/tzengyuxio/kaodata) — LS11 解压算法

## 技术细节

参见 [CLAUDE.md](CLAUDE.md)：LS11 位流规范、各 `.lzw` 的位图编码、Worldmap 块编码 + 后处理 pipeline。
