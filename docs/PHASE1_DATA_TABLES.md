# Phase 1: 数据表挖掘进度

> 目标：从 `Koukai2/*.dat` 提取游戏平衡数据为结构化 JSON，供新游戏使用。

## ✅ 已破解结构

### `Za_dat.dat` (2424 B) — 每港口数字 stats
- **101 records × 24 bytes** (= 12 u16 LE per port)
- 前 5 个 u16 总是有效（0-90 范围）= 基础属性（推测 5 种必备商品）
- 后 7 个 u16 含 `0xFFFF` 哨兵 = 该港口**不交易此商品**
- 总共 12 个商品 slot per port
- 字段语义待验证（需对照游戏内显示）
- ✅ 已导出 `output/game_data/za_dat.json`

### `Windcur.dat` (1350 B) — 全球风向/洋流模型 ⭐⭐⭐⭐⭐
- **30 cols × 45 rows = 1350 bytes** — **完美匹配 Worldmap 的 block grid**
- 每字节编码该海域 block 的风/流参数（可能 high nibble = direction, low nibble = strength）
- 值分布：0x00（陆地/无数据 75 个）、0x0a（79）、0x15（83）、0x22-0x3f 等
- 这是新游戏可以**直接用**的航海机制核心数据
- ✅ 已导出 `output/game_data/windcur_dat.json`

### `Monster.dat` (200 B) — 海怪 stats
- 实际数据约 160 字节（末尾零填充）
- 推测 25 × 8 bytes 或类似结构
- ✅ 已导出 `output/game_data/monster_dat.json`，需进一步分析具体字段

## 🟡 已映射但需深挖

### `Snr0-6.dat` (4-15 KB 各) — 剧本/事件脚本 ⭐⭐⭐⭐⭐
- **所有 7 个文件以 `SNDT` magic 开头**（"Scenario DaTa"）
- byte 4-5 有文件编号区别：Snr0=0x8000, Snr1-6=0x0000-0x0500
- 内部含 u32 BE 偏移表 + 子块结构
- JohanLi 的 `SNR1.MES` 就是这种文件，他能从中读出 dialog/event 文本
- **同样卡在繁体字 byte→tile mapping**——格式破了但内容显示不出来
- 这是事件**结构与逻辑**最丰富的文件，应该是 Phase 1 的次重点

### `Transit.dat` (22080 B) — 推测航线/转移规则
- 多种 stride 可能（16/24/32/48/64...）
- 第一个 record 看着像 "(byte, byte, byte, FF, FF, byte) × n" 模式
- 需进一步对齐

### `Colony.dat` (17700 B = 100 × 177) — 港口描述文本
- 字段：港口名（最多 7 个中文字符）+ 描述段落（多个 `81 31` / `81 34` 分隔）
- 内容是**百科描述**，不是数字 stats（数字在 Za_dat.dat）
- 同样卡在繁体字 mapping，无法显示

### `Hdat.put` (31624 B) — 推测动画/触发查找表
- 8 字节重复 stride，约 3953 条记录
- 模式如 `fe04 0004 be00 0000` 重复

### `End_put.dat` (40864 B) — 推测结局相关
- 起始 `00 44 00 00 44 00 00 44 ...` 重复 4 字节模式

### `Event0-6.dat` (8-62 KB 各) — 实为事件 CG 图
- 头部 `u32 BE offset table` + 块 `w/h header`
- ⚠️ 跟 Opgraph 同款内层压缩，**已在 ROADMAP 中放弃**（新游戏不需要原 CG）

## ⬜ 未触

| 文件 | 大小 | 推测 |
|---|---|---|
| `Menu.dat` | 2522 B | UI 菜单文本 |
| `Hdat.put` | 31624 B | 动画/触发？ |
| `End_put.dat` | 40864 B | 结局相关 |
| `Data1.lzw` 剩余 part | 各 | 船舶 stats（已知 part_0011 后半 = ship 图集） |

## 📊 当前 Phase 1 进度

```
✅ Za_dat.dat        — 港口数字 stats (结构完成，语义待验证)
✅ Windcur.dat       — 全球风向/洋流网格 (结构完成)
🟡 Monster.dat       — 海怪 stats (导出但语义未明)
🟡 Snr0-6.dat        — 剧本/事件 (格式破了卡字体)
⬜ Colony.dat        — 港口描述文本 (卡字体)
⬜ Transit.dat       — 航线 (未分析)
⬜ Hdat.put          — 待分析
⬜ End_put.dat       — 待分析
⬜ Menu.dat          — 待分析
⬜ Data1.lzw 其他 part — 船舶 stats 待找
🟥 Event*.dat        — 实为 CG 图 (放弃)
```

## 关键观察

1. **港口数 = 101**（Portmap + Za_dat 一致）
2. **风向网格 = 30×45 完全对齐 Worldmap block grid** — 巨大确认
3. **`0x81 0x31`/`0x81 0x34` 是文本段落分隔符**（在 Colony.dat 中重复出现）
4. **`SNDT` magic 标识 Scenario Data 文件家族**
5. **0xFFFF 是商品/物资的"不可用"哨兵**（Za_dat.dat 第 6+ 字段）

## 下一步建议

1. **深挖 Snr*.dat 结构**（事件脚本核心，但要先解决字体 mapping）
2. **分析 Transit.dat**（航海/路线机制）
3. **挖 Data1.lzw 剩余 part 找船舶 stats**

或者**先跳到 Phase 2 (Main.exe 公式)**——找到 byte→tile mapping 后顺便可以读懂所有文本，并扒出交易/海战公式。
