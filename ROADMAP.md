# 大航海2 逆向工程 — 路线图

> **终极目标**：用反向工程出来的**机制 + 数据**，做一个**"大航海"风格的现代游戏**。
> **不是**：复刻原作 / 搬运资源 / 做翻译。原作只是参考蓝本。

---

## 📊 当前进度总览

```
✅ Phase 0: 视觉资产           ████████████████████ 95%
✅ Phase 1: 数据表             █████████████████░░░ 85%  (raw 完成, semantic 80% 待补)
🟡 Phase 2: 公式 RE            ███░░░░░░░░░░░░░░░░░ 15%  (基础设施够, 深度按需做)
✅ Phase 3: 设计文档           ████████████████████ 100% (PHASE3_DESIGN_DOC.md)
🟡 Phase 4: 现代实现           █████░░░░░░░░░░░░░░░ 25%  (MVP 在 game/, 持续推进)
```

**当前位置**：Phase 4 推进中——在 `game/` 子目录里用 Godot 4 实现 MVP，用前 3 个阶段的 RE 产物作为数据源。

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

### 🟡 Phase 4 — 现代实现（25%, 在 `game/` 推进）

**已完成功能**：

| 模块 | 状态 | 细节 |
|---|---|---|
| Godot 4 项目结构 | ✅ | 1280×720 视口, Forward+, 自动 import |
| 世界地图 | ✅ | 从 RE'd Worldmap.lzw v2 |
| 10 港口标记 | ✅ | 红方块 + 名字标签 (坐标不准, 用户说先放) |
| 港口屏幕（点击进入）| ✅ | 港口大图 + governor 头像 + 商品列表 |
| 商品图标（12 种）| ✅ | 从 RE'd 128 disc 选 12 |
| Governor 头像 | ✅ | 从 RE'd 128 kao 头像选 10 |
| 港口大图 (10 个) | ✅ | 从 RE'd Portmap 101 缩到 512px |
| Buy/Sell 交易 | ✅ | 金币/库存实时更新 |
| 船 sprite + 移动 | ✅ | 三角形 + Line2D trail, 自动转向 |
| 船在港口间航行 | ✅ | 线性插值 80px/s 基础速度 |
| **风/洋流 overlay** | ✅ | 30×45 网格箭头, W 键切换显隐 |
| **风影响船速** | ✅ | 顺风 1.5x / 逆风 0.5x / 无风 1x |
| English UI | ✅ | 避开 CJK 字体问题 |
| 资产合并到主 repo | ✅ | sea_demo_new 已并入 `sea2_demo/game/` |

**未完成（待办）**：

| 模块 | 优先级 | 难度 |
|---|---|---|
| **航行事件**（风暴/海盗/商队/发现物）⭐ 下一步 | 高 | 中 (用 YAML 描述) |
| **海战系统**（hex grid + 风向影响）| 高 | 高 (用 Iap/Iae sprite) |
| 存档 / 多存档 | 中 | 低 |
| 港口坐标精修 | 低 | 低 (用户说放着) |
| CJK 字体加载（恢复中文 UI）| 低 | 低 |
| 扩展到全 101 港口 | 中 | 低 |
| 多种船只 + 升级 | 中 | 中 |
| 决斗系统（1v1 剑斗）| 中 | 中 (用 Iap sprite) |
| 美术换新（替换占位图）| 低 | 高 (需要美工) |
| BGM | 低 | 中 (借 JohanLi MIDI) |
| 多语言 / i18n | 低 | 中 |

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

## 🎯 下一步行动（即将开始）

**Phase 4 最高 ROI 任务：航行事件系统**

理由：
- 让游戏从"trading spreadsheet"变成真正的游戏
- 用得上闲置的 RE 资产（Iap/Iae 875 决斗 sprite, disc 128 道具图标, Char 72 NPC sprite）
- 不依赖坐标准不准（事件是航行途中触发）
- YAML/JSON 驱动，方便后续加事件

具体实现：
1. 船航行中按距离/时间触发随机事件
2. 事件类型：风暴 / 海盗遭遇 / 过路商队 / 岛屿发现 / NPC 邀约
3. 事件 UI：左侧 portrait/icon + 右侧描述 + 2-3 个选项按钮
4. 事件数据：YAML 文件描述（参考 PHASE3 设计文档的 DSL）

---

## 🗂️ 相关文档

- 项目首页：[README.md](README.md)
- 项目约定 + 已破解格式规范：[CLAUDE.md](CLAUDE.md)
- Phase 1 数据表笔记：[`docs/PHASE1_DATA_TABLES.md`](docs/PHASE1_DATA_TABLES.md)
- Phase 2 RE 笔记：[`docs/PHASE2_PROGRESS.md`](docs/PHASE2_PROGRESS.md), [`docs/REVERSE_ENGINEERING_NOTES.md`](docs/REVERSE_ENGINEERING_NOTES.md)
- Phase 3 新游戏 spec：[`docs/PHASE3_DESIGN_DOC.md`](docs/PHASE3_DESIGN_DOC.md)
- Phase 4 游戏：[`game/`](game) + [`game/README.md`](game/README.md)
- 数据浏览（HTML 表格）：[`docs/DEMO_TABLES.md`](docs/DEMO_TABLES.md)
