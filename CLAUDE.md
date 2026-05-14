# CLAUDE.md

Context for future Claude sessions in this repo. Read this before suggesting changes.

## What this repo is

逆向《大航海時代II》(KOEI, 1993, PC-9801) 资源文件。源文件不在 git 里——本地路径 `/Users/dong/Projects/Koukai2/`。

**当前状态（资源出土进度）**：
- `Kao.lzw` 全部解出（80×64 头像 + 48×48 发现物/道具精灵）
- `Portchip.lzw` 解出（7 atlas × 240 tiles × 16×16 4bpp）
- `Portmap.lzw` × `Portchip.lzw` 完整渲染——101 个真港口地图全部出图
- `Worldmap.lzw` 渲染成功（含 v2 后处理：沙漠填充、海岸 LUT、frigid/temperate 色带）
- `Iap1-6.lzw` + `Iae1.lzw` 解出——875 张决斗 sprite（6 玩家角色 + 1 敌人）
- `Char.lzw` 解出（不是字体，是 7 角色 walking sprite 共 72 帧，参考 JohanLi 的 `portraits-items-discoveries/char.py`）
- LS10 magic 跟 LS11 算法相同（已加入解码器允许列表）
- 未触：`Data1.lzw` 剩下的 part（船舶、UI、人物动画等）
- **卡住：`Opgraph.lzw` 14 part = 事件 CG**，结构搞清楚但内层 4bpp + 0x38-escape 压缩没破

**发现 `Koukai2/` 还有一堆非 LZW 事件文件**（之前没看过）：
- `Graph.dat` (445KB, 65 张事件 CG, 含 640×400 全屏) + `Graph2.dat` (78KB)
- `Endgrp.dat` (399KB, 59 张 224×160 结局图)
- `Event0.dat` ~ `Event6.dat` (8-62KB 事件脚本/触发表)
- `Message.dat` (29KB 对话文本)
- `1.pat` `2.pat` (173/217KB 字体或 tile pattern)
- `D2.mml` (28KB BGM 谱), `Fmdrv.com` (FM 音源驱动)
- `Colony.dat`/`Monster.dat`/`Transit.dat`/`Windcur.dat`/`Za_dat.dat`/`Snr*.dat` 等数据表

**反汇编进度**（`Main.exe` 298KB, PC-98 16-bit MZ）：
- 事件 CG 解码器**已定位**（入口 0x5e00），结构搞清楚：4bpp packed + 0x38 escape + per-image 16-entry 派发表 + 4-plane VRAM 直写
- Python 移植**还没做**——详细反汇编笔记在 [`docs/REVERSE_ENGINEERING_NOTES.md`](docs/REVERSE_ENGINEERING_NOTES.md)，完整 disasm 在 [`docs/main_exe_decoder_disasm.txt`](docs/main_exe_decoder_disasm.txt)
- 工具：Ghidra 12.1 (`/opt/homebrew/Cellar/ghidra/12.1/`) + capstone Python 包

参考实现：[github.com/JohanLi/uncharted-waters-2-research](https://github.com/JohanLi/uncharted-waters-2-research) 救命——`tileset_regular.py` 直接给出了 4bpp / 1024-bit-block 编码。该 repo 还有 `tileset_large.py` (DATA1.018)、`tileset_ship.py` (DATA1.011 后半)、`dueling/extract_iap.py`、`world_map_processing.py` 等可继续 mine。

纯粹的资源逆向。

## What worked (canonical pipeline)

1. `scripts/ls11_decode.py <file.lzw> <out_dir>` — KOEI LS10/LS11/Ls12 解压（同一算法，三种 magic）
2. `scripts/inventory_lzw.py` — 批量解压全部 `.lzw` 到 `output/lzw_parts/`，打印 part 数量/大小分布
3. `scripts/render_kao_v4.py` — 80×64 / 8色 / 3-plane 头像
4. `scripts/render_disc_v1.py` — 48×48 / 8色 / 3-plane 发现物
5. `scripts/render_portchip_v2.py` — 16×16 / 4bpp / 16色 港口 chip atlas
6. `scripts/render_portmap_v2.py` — 用 Portchip atlas 真贴出 101 个港口的 1536×1536 全图
7. `scripts/render_worldmap_v1.py` — 用 Data1 part_0011（regular tileset）+ part_0018（large tileset 索引）拼出 3 张世界图

输出：
- `output/contact_kao_v4.png` — 头像
- `output/contact_disc_v1.png` — 发现物/道具
- `output/portchip_v2/part{0-6}_atlas.png` — 7 套 chip atlas
- `output/portmap_v2/{000-100}.png` + `output/contact_portmap_v2.png` — 101 个港口真图
- `output/worldmap_v1/part{0-2}_thumb.png` + `output/contact_worldmap_v1.png` — 3 张世界图 1px/tile 缩略
- `output/worldmap_v1/part{0-2}_4xtile.jpg` — 同上 4px/tile JPEG 详图（每张 ~1.5MB，故 JPEG q=85，不在脚本中 Read 回来以避开 API 大小限制）

## What did NOT work (don't redo)

`scripts/experiments/` 里的全部尝试都试过且失败了。简记：

| 文件 | 假设 | 为什么错 |
|---|---|---|
| `decode_lzw.py` | 标准 LZW 变长码 | KOEI 用的是变长前缀码 + 自定义字典，不是 LZW |
| `decode_ls11.py` | 字节对齐 LZSS (6 种参数组合) | LS11 不是 LZSS，是位流前缀码 |
| `decode_bitlzss.py` | 位对齐 LZSS (144 种参数组合) | 同上，算法根本不是 LZSS 系列 |
| `render_kao.py` (v1) | 4-plane 16色 planar (PC-9801 典型) | 实际是 3-plane 8色，stride 也不同 |
| `render_kao_v2.py` | 6 种 chunky 4bpp 变体 | 同上 |
| `render_kao_v3.py` | 把 part 内部拆/或 part[i]+part[i+128] 拼一起 | 后 128 个 part 是别的东西（864 字节，可能是物品/小图标），不是头像的另一半 |

**根本经验**：盲试参数浪费大量时间。先 GitHub 搜「<file ext> format」、找现成解码器（tzengyuxio, JohanLi 这类），比对位流细节快几十倍。

## Format spec (verified)

### LS11 / Ls12 压缩

```
bytes 0-3    : magic "LS11" 或 "Ls12"
bytes 4-15   : reserved (零)
bytes 16-271 : 256 字节自定义字典（每文件独立！）
bytes 272+   : 12 字节大端 index 记录:
               (compressed_size: u32, uncompressed_size: u32, offset: u32)
               以 4 个零字节结束
data area    : 压缩 part 数据，offset 是绝对偏移
```

位流解码（大端，MSB first）：
- 读 bit 直到遇到 0 → `mask_len` = 读了几个 bit
- 再读 `mask_len` bits → `factor`
- `code = (2^mask_len - 2) + factor`
- 若 `code < 256` → 输出 `dictionary[code]`
- 若 `code >= 256` → 设 `delta = code - 256`；下一个 code 解码出的值 `+3` 作为长度，从当前输出回退 `delta` 字节复制

### Kao.lzw 位图（头像 + 发现物，共用编码）

- 解压出 256 个 part：前 128 个 = 1920 字节（80×64 头像），后 128 个 = 864 字节（48×48 发现物/道具）
- 编码方案完全一样：3-plane 8 色 planar，按 8 像素块组织
- 每个 8 像素块占 24 bits：`bits[p..p+8]` 是 plane 0，`bits[p+8..p+16]` 是 plane 1，`bits[p+16..p+24]` 是 plane 2
- 像素 j (0..7) 的颜色索引 = `(plane0[j]<<2) | (plane1[j]<<1) | plane2[j]`
- pointer `+= 24` 进下一块
- 头像：80 行 × 8 块/行 = 640 块 = 15,360 bits = 1920 字节
- 发现物：48 行 × 6 块/行 = 288 块 = 6,912 bits = 864 字节

### Portchip.lzw 位图（与 Data1 同款）

- 14 parts：交替的 7×30720 字节图集 + 7×4 字节调色板元数据
- 每图集 30720 字节 = 240 tiles × 128 字节/tile
- tile = 16×16 像素 / 4 bpp / 16 色
- 编码：1024-bit 块（一个 tile = 一个块），256 个像素，每像素 4 bits 按 stride=256 散开：
  - 像素 `i` 的颜色索引 = `(block[i]<<3) | (block[i+256]<<2) | (block[i+512]<<1) | block[i+768]`
- 16 色调色板有 dawn/day/dusk/night 四套（JohanLi 给出），代码里用 "day"
- 4 字节小 part 还没解：怀疑是 sub-palette 或 master-palette 索引，色彩略偏但不影响形状识别

### Portmap.lzw（港口 tile 索引）

- 101 parts × 9216 字节 = 96×96 tile 索引数组（行优先）
- 每字节值范围 0..239，正好对应 Portchip 一个 atlas 的 240 个 tile
- 港口→atlas 映射在 **`Chip_no.dat`**（100 字节，每字节 = atlas 索引 0..6；端口 100 无对应条目，回退到 atlas 0）
- 完整 101 个港口已渲染，气候/建筑风格按 `Chip_no.dat` 正确分配

### Worldmap.lzw（世界地图）

- 3 个大 part，每个 ~22-25KB；LS11 解压后还有一层**块编码**（不是普通 RLE）
- 前 2700 字节是 header（暂未细究——可能是城市/特殊地物坐标表），从 byte 2700 开始进入位流
- 位流分 1350 个 block（45 行 × 30 列），每 block 描述一片 12×12 large-tile-index 区域
- 每 block 的 8-bit header：bit 0 = is_diff，bit 5-7 = template number 0..4
  - template 0..3 = 半屏填充 15（沙漠？陆地？），template 4 = 全 15，template 都是 12×12
  - 若 is_diff=1：再读 144 bits 作 correction mask，然后对每个 mask=1 的位置读 8 bits 作为 large-tile 索引覆盖 template
- 解出来是 (45, 30, 12, 12) → reshape 成 540×360 large-tile 网格 → 每个 large tile = 2×2 regular tile → 最终 1080×720 regular-tile 网格
- **Large tileset**: Data1 `part_0018` (1024 字节，256 项)。前 16 项特殊（按 i 的 4 个 bit 填 0/65），后 240 项每项 4 字节直读，> 128 的字节值视作 0
- **Regular tileset**: Data1 `part_0011` 的前一半（32768/2 = 16384 字节）。编码同 Portchip——1024-bit 块，4bpp，stride-256 散开。共 128 个 16×16 tile
- 调色板沿用 Portchip 的 16 色 day-palette
- v1 = 纯 tile 拼图（基础渲染，海岸有锯齿）；v2 = v1 + JohanLi 的后处理：
  - `fill_deserts`: tile 89 沿 +x/+y 扩散覆盖 tile 65（草地）
  - `replace_coasts`: 水 tile (0) 用 `Data1 part_0010`（512 字节 coast LUT）按 8 邻居 land 位图查找替换
  - `replace_desert_coasts`: 沙漠边的水 tile +24 偏移变沙漠岸
  - `update_frigid_temperate`: 前/后 24 行（极地）grass +16；中段第 24..14×24 和 31×24.. 行（温带）grass +8
  - `manual_corrections`: part 0 / part 2 共 5 处硬编码 tile 修正

调色板（来自 JohanLi）：
```
0=#000000 1=#00A060 2=#D04000 3=#F0A060
4=#0040D0 5=#00A0F0 6=#D060A0 7=#F0E0D0
```

## 还能做什么

详细 6 阶段路线图见 [ROADMAP.md](ROADMAP.md)。

**当前 3 个甜区任务**（完成后大航海2 资源 100% 出土）：
1. **完成 Main.exe 事件 CG 解码器 Python 移植** — 笔记齐了在 `docs/`，移植后能解 `Graph.dat`（65 张）+ `Endgrp.dat`（59 张）+ `Opgraph.lzw`（共 ~130 张事件 CG）
2. **挖 `Event*.dat` + `Message.dat`** — 剧情/对话/触发逻辑（写剧情百科）
3. **`D2.mml` 转 MIDI** — 一晚上拿全部 BGM（JohanLi 已经做过可参考）

**副产品**：同样的 LS11 解码器可应用于三国志IV `MAINMAP.S4` 等其他 KOEI 老作

## 项目约定

- 脚本路径都用 `Path(__file__).resolve().parent.parent` 做 repo-relative，不要写绝对路径。
- `output/` 全部由脚本生成，不在 git 里。
- `experiments/` 是历史记录，不要删，但也不要再加新的失败尝试（直接改 v4 / 新加 v5 即可）。
- 用户偏好简短回复，看图说话——渲染完直接 Read 出 PNG 给他看。
