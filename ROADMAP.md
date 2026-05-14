# 大航海2 全面逆向 — 路线图

按 **价值 / 难度比** 从高到低排，6 个阶段。当前位置：阶段 1 收尾 + 阶段 5 已部分开工（事件 CG 卡在解码器内层）。

---

## ✅ 阶段 0：压缩格式破解（已完成）

- `LS10` / `LS11` / `Ls12` 三种 magic 解压器（`scripts/ls11_decode.py`）
- 自定义 256 字节字典 + 变长前缀位流 + 回溯复制
- 批量解压所有 `.lzw` → `output/lzw_parts/`（`scripts/inventory_lzw.py`）

## 🟢 阶段 1：剩余资产抽取（~95% 完成）

| 文件 | 内容 | 参考 | 状态 |
|---|---|---|---|
| `Kao.lzw` | 128 头像 + 128 发现物/道具 | 自研 | ✅ |
| `Portchip.lzw` | 7 atlas × 240 tile 港口素材 | `tileset_regular.py` | ✅ |
| `Portmap.lzw` | 101 港口 + `Chip_no.dat` atlas 映射 | 自研 | ✅ |
| `Worldmap.lzw` | 3 张世界地图 + 沙漠/海岸/极地后处理 | `world_map_processing.py` | ✅ |
| `Iap1-6.lzw` `Iae1.lzw` | 6 玩家 + 1 敌人决斗 sprite，共 875 帧 | `dueling/extract_iap.py` | ✅ |
| `Char.lzw` | 7 角色走路 sprite，共 72 帧（非字体！）| `portraits-items-discoveries/char.py` | ✅ |
| `Data1.lzw` 剩余 part | 船舶图集（part_0011 后半）、UI 元素 | `tileset_ship.py` | ⬜ TODO |
| `Opgraph.lzw` | 14 part，事件 CG（开场/谒见王/婚礼等）| **无参考** | 🟥 内层压缩没解 |

## 🟡 阶段 2：数据表（~3-7 天，难度中，价值最高）

`/Users/dong/Projects/Koukai2/` 里**直接可读**的 `.dat` 文件——大部分还没碰：

### 已识别
- `Chip_no.dat` (100 B) — port → atlas 索引映射 ✅

### 待挖（事件/数据相关）
- **`Event0.dat` ~ `Event6.dat`** (8-62 KB) — 事件脚本/触发表 ⭐
- **`Message.dat`** (29 KB) — 对话/UI 文本 ⭐
- `Colony.dat` (17 KB) — 殖民地数据
- `Monster.dat` (200 B) — 海怪数据
- `Transit.dat` (22 KB) `Windcur.dat` (1.4 KB) `Za_dat.dat` (2.4 KB) — 风/洋流/事件参数
- `Snr0.dat` ~ `Snr6.dat` — 不明（人物名册？）
- `Hdat.put` `End_put.dat` — 不明
- `1.pat` `2.pat` (173/217 KB) — 字体或 tile pattern ⭐

### 待挖（游戏数据表，需配合存档 diff）
- 港口属性表（位置、物资、价格、统治者、人口）
- 商品定义（13 种贸易物品基价/波动区间/产地）
- 船只参数（容量、速度、火炮、耐久、价格）
- 人物属性表（提督、副官、酒馆雇佣兵）

**方法**：hex dump 找 stride，交叉验证（港口=101，舰船≈30-40，商品=13）

## 🟢 阶段 3：存档格式（~1-3 天）

- DOSBox 起游戏，建几个 save，diff 定位字段
- KOEI save 通常简单线性结构
- 产出：存档编辑器 + 验证阶段 2 字段含义

## 🟡 阶段 4：音乐（~2-5 天）

- `D2.mml` (28 KB) — **就是 MML 格式 BGM 谱**，可直接转 MIDI/MP3
- `Fmdrv.com` (5 KB) — FM 音源驱动
- PC-9801 OPN/OPNA，工具：`pmdwin` / `FMPMD2000`
- JohanLi 已经做过这个（见 `music/converted/*.mp3`），可参考

## 🟠 阶段 5：游戏逻辑反汇编（已部分开工）

主程序是 **`Main.exe`**（298KB，PC-98 16-bit 实模式 MZ），不是 KOUKAI2.EXP。还有 `Open.exe`（开场）、`End.exe`（结局）。

### 进度
- ✅ Ghidra 12.1 + capstone 已装
- ✅ MZ 头解析（code 段从 0x5200 起）
- ✅ **事件 CG 解码器定位** — 函数入口 0x5e00
- ✅ 解码器结构搞清楚：4bpp packed + 0x38 escape + per-image 16-entry 派发表 + PC-98 4-plane VRAM 直写
- ⬜ Python 移植解码器（估计 2-4 小时聊天往返）
- ⬜ 还要解的核心公式：交易价格波动、海战 hit/damage、探险概率、忠诚度/叛变

详细笔记：[`docs/REVERSE_ENGINEERING_NOTES.md`](docs/REVERSE_ENGINEERING_NOTES.md)
完整反汇编：[`docs/main_exe_decoder_disasm.txt`](docs/main_exe_decoder_disasm.txt)

## 🔴 阶段 6：开源复刻（数月～年）

基于阶段 1-5 的全部产出，用现代引擎重写。OpenTTD / OpenMW 路线，社区工程。

---

## 当前甜区

- **完成阶段 5 的解码器移植** → 直接拿到所有事件 CG（**`Graph.dat` + `Endgrp.dat`**，共 65+59=124 张全屏图）
- **挖 `Event*.dat` + `Message.dat`** → 拿到对话剧本和事件触发逻辑（剧情百科可做了）
- **`D2.mml` 转 MIDI** → 一晚上拿到全部 BGM
- 这三项做完，大航海2 资源就**100% 出土**
