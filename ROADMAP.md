# 大航海2 逆向工程 — 路线图

> **终极目标**：用反向工程出来的**机制 + 数据**，做一个**"大航海"风格的现代游戏**。
> **不是**：复刻原作 / 搬运资源 / 做翻译。原作只是参考蓝本。

---

## 📊 当前进度总览

```
✅ Phase 0: 视觉资产           ████████████████████ 95%
✅ Phase 1: 数据表             ██████████████████░░ 90%  (船/港/风/事件全在 JSON 里)
🟡 Phase 2: 公式 RE            ███░░░░░░░░░░░░░░░░░ 15%  (按需做)
✅ Phase 3: 设计文档           ████████████████████ 100%
🟡 Phase 4: 现代实现           ███████░░░░░░░░░░░░░ 35%  ← 进 game/, 已有完整航行/事件/战斗循环
```

**当前位置**：Phase 4 在 `game/` —— 玩法已经成型（航行、风向、贸易、随机事件、海战）。

**下一步**（接下来按这顺序自动推进）：
1. 多船型 + 港口买船（用 25 ships stats）
2. 1v1 决斗（boarding 后用 Iap/Iae 决斗 sprite）
3. 存档系统
4. 更多港口（从 10 扩到 30+）
5. 港口坐标精修（一直推迟，可能批量调）

---

## 🧭 设计哲学

| ❌ 误区 | ✅ 正解 |
|---|---|
| "把所有资源提取出来" | "理解游戏机制 + 拿到平衡数据" |
| 美术资产逐字节复刻 | 美术全新自做，原作只做风格参考 |
| 翻译每条对话 | 理解事件结构，剧情新写 |
| 卡在 Opgraph 压缩 | 跳过，因为新游戏不需要原图 |
| 完整破 BGM 编码 | 听几首确定音乐风格就行 |

---

## ⭐ 价值矩阵

| 工作内容 | 价值 | 状态 |
|---|---|---|
| **`.dat` 数据表** | ⭐⭐⭐⭐⭐ | 🟡 关键文件已抽（Za_dat, Windcur, Monster）+ raw dump 全 |
| **Main.exe 公式** | ⭐⭐⭐⭐⭐ | 🟡 基础设施识别，深度公式按需做 |
| 数据格式破解 LS11 | ⭐⭐⭐ | ✅ 完成 |
| 视觉资产 | ⭐⭐ | ✅ 95% |
| 对话文本 + 字体表 | ⭐⭐ | 🟡 字节对了, 字符 mapping 未解 (放弃) |
| 事件 CG | ⭐ | 🟥 卡内层压缩 (放弃) |
| BGM | ⭐ | 🟥 没碰 (放弃) |

---

## 📋 5 阶段详细状态

### ✅ Phase 0 — 视觉资产（基本完成）

- ✅ LS10/LS11/Ls12 解压器 + 批量解压所有 `.lzw` (`scripts/ls11_decode.py`)
- ✅ Kao 128 头像 (80×64) + 128 发现物/道具 (48×48)
- ✅ Portchip 7 atlas × 240 tile (16×16 4bpp)
- ✅ Portmap 101 港口大图 (96×96 tile = 1536×1536 px)
- ✅ Worldmap 3 张世界图 + v2 后处理（沙漠/海岸/极地）
- ✅ Iap/Iae 875 决斗 sprite（6 玩家 + 1 敌人）
- ✅ Char 72 NPC walking sprite
- ✅ 2.pat 6800 繁体字模（mapping 未解，但 atlas 可见）

**后续不再投入**——已经够当风格参考了。

### 🟡 Phase 1 — 数据表（85%, 关键文件已破）

| 文件 | 大小 | 内容 | 状态 |
|---|---|---|---|
| `Za_dat.dat` | 2.4 KB | **101 港 × 12 商品 stats** | ✅ 已抽 JSON (`output/game_data/za_dat.json`) |
| `Windcur.dat` | 1.4 KB | **30×45 风/洋流网格** | ✅ 已抽 + 在新游戏里实际使用 |
| `Monster.dat` | 200 B | 海怪 stats | ✅ raw 已抽 (字段语义待补) |
| `Chip_no.dat` | 100 B | 港口→atlas 映射 | ✅ 已用于 portmap 渲染 |
| `Colony.dat` | 17 KB | 港口名+描述文本 | 🟡 结构破了, 文本卡字体 |
| `Snr0-6.dat` | 4-15 KB 各 | 剧本/事件脚本 | 🟡 SNDT magic 识别, 内容卡字体 |
| `Transit.dat` | 22 KB | 航线/转移 | 🟡 4-byte 对齐结构识别, 语义未确认 |
| `Hdat.put` | 32 KB | 动画/查找表? | 🟡 raw 已抽, 语义 unknown |
| `End_put.dat` | 41 KB | 结局相关? | 🟡 raw 已抽 |
| `Menu.dat` | 2.5 KB | UI 菜单文本 | 🟡 raw 已抽, 卡字体 |
| `Data1.lzw` 剩余 part | 各 | 船舶 stats / UI / 动画 | 🟡 全 raw 已抽, semantic 部分识别 |
| **`KOUKAI2.DAT`** | 329 KB | **主数据文件** | 🟡 发现 + 头部识别 (情景启动), 深挖待办 |
| `Event*.dat` | 8-62 KB 各 | 实为事件 CG 图 (不是脚本) | 🟥 同 Opgraph 压缩, 放弃 |

详见 [`docs/PHASE1_DATA_TABLES.md`](docs/PHASE1_DATA_TABLES.md)。

### 🟡 Phase 2 — Main.exe RE（15%, 基础设施识别后暂停）

**已识别**：
- ✅ MZ 头解析 / 5 个段 / 文件 wrapper @ 0x521c
- ✅ 事件 CG 解码器入口 @ 0x5e00（4bpp + 0x38 escape + 16-mode 派发）
- ✅ 消息显示函数 @ 0x27f62
- ✅ KOUKAI2.DAT 主数据文件
- ✅ 字符串段 0x3815

**未做**（按需启动）：
- ⬜ 贸易价格波动公式
- ⬜ 海战命中/伤害公式
- ⬜ 风向影响速度公式
- ⬜ 事件触发 / 探险概率 / 忠诚度

详见 [`docs/PHASE2_PROGRESS.md`](docs/PHASE2_PROGRESS.md), [`docs/REVERSE_ENGINEERING_NOTES.md`](docs/REVERSE_ENGINEERING_NOTES.md)。

**判断**：单人项目 Phase 2 深度提取 ROI 偏低——直接用 Phase 1 数据 + 经验型公式做 Phase 4，遇到具体需求再回头挖单个公式。

### ✅ Phase 3 — 设计文档（完成）

[`docs/PHASE3_DESIGN_DOC.md`](docs/PHASE3_DESIGN_DOC.md)：320 行新游戏 spec
- 世界设计（真实/架空/随机生成 3 选项）
- 5-8 种船型简化方案
- 11 种商品 + 价格公式
- 海战 / 决斗子系统
- 事件 DSL (YAML 风格)
- 推荐 **Godot 4 + 2D 像素艺术**
- MVP → Beta → v1 路线图

### 🟡 Phase 4 — 现代实现（35%, 在 `game/` 推进）

**✅ 已完成功能**：

| 模块 | 细节 |
|---|---|
| Godot 4 项目结构 | 1280×720 视口, Forward+ |
| 世界地图 | RE'd Worldmap.lzw v2 |
| 10 港口标记 | 红方块 + 名字 (坐标不准, 已知) |
| 港口屏幕 | 港口大图 + governor 头像 + 商品列表 |
| 12 种商品 + 图标 | 价格 50-500g 合理范围 |
| 10 governor 头像 | 从 128 Kao 选 |
| Buy/Sell 交易 | 金币/库存实时 |
| **真船 sprite + 动画** | 32 个 RE'd 船图, 0.4s 帧切换, 镜像翻转 |
| 船导航 | 港口间线性插值 |
| 风/洋流 overlay | 30×45 网格箭头, W 键切换 |
| 风影响船速 | 顺风 1.5x / 逆风 0.5x |
| Hull 耐久 UI | 顶部 Label, 事件影响 |
| **🆕 航行事件系统** | 8 模板 (海盗/风暴/商人/岛屿/学者/...) 4%/sec 触发 |
| **🆕 海战** | 双 HP 进度条, 3 行动 (Cannon/Aimed/Flee), 胜败结算 |
| 25 船 stats 数据 | data/ships.json (容量/火炮/价格/耐久) |
| 128 人物目录 | data/characters.json 7 大类 |

**⬜ 未完成（按优先级）**：

| # | 模块 | 优先级 | 难度 | 已有素材 |
|---|---|---|---|---|
| 1 | **多船型 + 港口买船** ⭐ 下一步 | 高 | 中 | 32 ship sprite + 25 stat 已就位 |
| 2 | **1v1 决斗**（boarding 后剑斗）| 高 | 高 | 875 Iap/Iae sprite |
| 3 | **存档 / 多存档** | 中 | 低 | - |
| 4 | **更多港口**（10→30+→101）| 中 | 低 | 101 portmap 全部已在 RE 库 |
| 5 | **港口坐标精修** | 低（用户放着）| 低 | - |
| 6 | **更好的图标匹配** | 低 | 中 | 128 disc，需人工选 |
| 7 | **NPC 走动**（港口里）| 中 | 中 | 72 Char sprite |
| 8 | **月/时间系统** | 中 | 中 | - |
| 9 | **CJK 字体** | 低 | 低 | - |
| 10 | **美术换新** | 低 | 高 | - |
| 11 | **BGM** | 低 | 中 | JohanLi MIDI |
| 12 | **i18n** | 低 | 中 | - |

**当前完整游戏循环**：起步港口 → 买货 → 起航 → 航行触发事件（含海战）→ 抵达 → 卖货 → 赚差价 ✓ 已能跑

详见 [`game/README.md`](game/README.md)。

---

## 🟥 已明确放弃 / 降优先级

| 工作 | 为什么放弃 |
|---|---|
| **Opgraph.lzw 事件 CG 解码** | 自定义压缩, 破解要数天; 新游戏不需要原图 |
| **Message.dat 字符 mapping** | 卡自定义字体表; 新游戏可以新写剧本 |
| **Event*.dat 解码** | 实为 CG 图, 同 Opgraph 卡, 非脚本表 |
| **D2.mml → MIDI** | 听一下风格就够; JohanLi 已有社区 MIDI |
| **完整反汇编 Main.exe** | 只挑核心公式, 不必反整个 EXE |
| **Iap/Iae sprite 进一步处理** | 已够用作素材 |

---

## 🎯 下一步行动（按这顺序自动推进）

1. **多船型 + 港口买船** —— 港口屏多个 "Shipyard" tab，列 5-10 艘船 stats 让玩家买。换船后 sprite/容量/火炮全变。**用 25 ship stats**。
2. **1v1 决斗** —— 海战胜利后可选"接舷战"，弹出 1v1 剑斗界面，玩家 vs 海盗船长。**用 875 Iap/Iae sprite**。
3. **存档 / 加载** —— 单一存档先做：Save 按钮 → JSON 写到 user://save.json。
4. **扩展港口** —— 从 10 → 30 → 101。批量校准坐标。
5. **时间/月份系统** —— 每段航行消耗 N 天，月份循环影响风向/价格波动。
6. **NPC 走动** —— 港口屏幕里几个 Char sprite 在角落踱步（纯氛围）。

---

## 🗂️ 相关文档

- 项目首页：[README.md](README.md)
- 项目约定 + 已破解格式规范：[CLAUDE.md](CLAUDE.md)
- Phase 1 数据表笔记：[`docs/PHASE1_DATA_TABLES.md`](docs/PHASE1_DATA_TABLES.md)
- Phase 2 RE 笔记：[`docs/PHASE2_PROGRESS.md`](docs/PHASE2_PROGRESS.md), [`docs/REVERSE_ENGINEERING_NOTES.md`](docs/REVERSE_ENGINEERING_NOTES.md)
- Phase 3 新游戏 spec：[`docs/PHASE3_DESIGN_DOC.md`](docs/PHASE3_DESIGN_DOC.md)
- Phase 4 游戏：[`game/`](game) + [`game/README.md`](game/README.md)
- 数据浏览（HTML 表格）：[`docs/DEMO_TABLES.md`](docs/DEMO_TABLES.md)
