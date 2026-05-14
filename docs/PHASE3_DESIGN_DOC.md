# Phase 3: 新游戏设计文档

> 基于大航海 II 逆向出来的**数据**和**机制**，外加经典大航海玩法理解，定义一个**风格相似、机制独立**的现代版海洋探险/贸易游戏的设计 spec。
>
> **不是复刻**。原作是参考。

---

## 🎯 高层定位

| 维度 | 大航海 II (1993, KOEI) | 新游戏 |
|---|---|---|
| **平台** | PC-9801 / 16-bit | Web (Godot HTML5) / Desktop |
| **画风** | 16×16 像素 / 16 色 | 现代像素艺术 OR low-poly 3D |
| **视角** | 2D 俯视 + 港口侧视 | 同（保留传统）|
| **核心循环** | 探险 / 贸易 / 战斗 / 故事 | 同 |
| **时代** | 大航海时代（15-16 世纪）| 同（可考虑加架空版本/多时代）|
| **流程** | 单线主角剧情 + 自由探险 | **更开放**：随机种子世界 + 模块化任务 |
| **存档** | 单存档 / 长线 | 多存档 + 短局选项（roguelike 元素）|

**核心 vibe**：自由航海 / 贸易策略 / 冒险发现 / 海战。

**取舍**：原作的强叙事 + 多主角剧情属于 1993 年单机产品的设计哲学。新游戏更倾向**可重玩性优先**——随机化世界，多种胜利条件，单局可短可长。

---

## 🌍 世界设计

### 地图

借鉴：大航海 II 的世界是**真实世界地图**（亚欧非美澳，约 1080×720 tile），分 3 张分屏。

**新游戏选项**：
- **A 选项**：真实地球地图（教育性强）
- **B 选项**：架空大陆（设计自由度高，避免历史敏感）
- **C 选项**：**随机生成大陆**（roguelike-friendly，可重玩）⭐ 推荐

### 港口

借鉴：原作 **101 个港口**，分 7 类气候/建筑风格（Chip_no.dat 映射）。

**新游戏**：
- 30-80 个港口（看场景大小可调）
- 每港口属性（参考 Za_dat.dat 结构）：
  - 基础 stats: 5 个必备资源（食物/水/木材/武器/纺织？）
  - 7 个可选商品 slot（0xFFFF = 不交易）
  - 统治者 / 港口规模 / 文化区域 / 防御力 / 人口

### 风向洋流

借鉴：原作 `Windcur.dat` 30×45 网格映射到 worldmap block，每字节编码风向 + 强度。

**新游戏**：
- 在每个海域块（hex 或方格）存储 `(wind_direction, wind_strength, current_direction, current_strength)`
- 角度可以是 4-bit (16 方向) 或更细
- **季节性变化**：原作有月份系统，季风方向变化（推测，需 Phase 2 后续证实）

---

## 🚢 船只系统

### 借鉴大航海 II 的船种

原作分两大类：
- **战舰**（Galleon, Frigate, Frigatta, etc.）—— 火力强、慢
- **商船**（Caravel, Carrack, Galley, etc.）—— 载货多、灵活

每船有 stats：
- 容量（吨位）
- 火炮数
- 船员数
- 速度（基础速度，受风向影响）
- 耐久度
- 价格

### 新游戏分类（简化版）

| 类别 | 数量 | 容量 | 火炮 | 速度 | 用途 |
|---|---|---|---|---|---|
| 渔船 | 1 | 小 | 0 | 中 | 起步 |
| 小型商船 | 1-2 | 中 | 0-4 | 中 | 早期贸易 |
| 大型商船 | 1-3 | 大 | 4-12 | 慢 | 主力贸易 |
| 战舰 | 1-2 | 中 | 12-30 | 中 | 海战 |
| 旗舰 | 1 | 大 | 20-40 | 中 | 后期主力 |

建议 5-8 种船型（不超过）。

---

## 💰 贸易系统

### 借鉴

大航海 II 有 **~13 种贸易品**：粮食、武器、布匹、香料、染料、矿物、珠宝、艺术品、酒、奴隶（敏感，去掉）等。

价格机制（推测，需 Phase 2 验证）：
- 每港口有该商品的"基价"
- 实际价格 = 基价 × (1 + 浮动) × (供需调整)
- 库存量影响价格
- 季节 / 事件可能改变基价

### 新游戏机制

**商品池（建议）**：
- 食物、香料、丝绸、铁矿、宝石、艺术品、酒、瓷器、毛皮、咖啡、烟草（11 种）
- 去掉历史敏感商品（奴隶）

**定价**（建议公式）：
```
display_price = base_price[port][good] * supply_factor * (1 + market_noise)
supply_factor = 1.0 / (1.0 + 0.05 * recent_buys - 0.03 * recent_sells)
market_noise = sin(day_in_year / 30) * 0.1 + random(-0.05, 0.05)
```

每个港口对每种商品有：
- `base_price`：基础价格
- `production_rate`：每月增加多少库存（产地→高，非产地→0）
- `consumption_rate`：每月消耗多少库存

---

## ⚔️ 战斗系统

### 海战（借鉴 + 简化）

大航海 II 海战是**回合制 + 风向角度**模型：
- 自己 vs 对手 N 艘船编队
- 每回合选行动（前进 / 转向 / 开炮 / 接舷战）
- 风向影响行动力
- 距离 / 角度影响命中

**新游戏建议**：
- 战术地图（hex 或 grid）
- 风向用箭头表示
- 顺风加速，逆风慢
- 火炮射程基于船型
- 命中 = (技能 + 距离修正 + 风向修正) - 闪避
- 击破船体 / 击毁火炮 / 接舷夺船 多种胜利方式

### 决斗（borrowed from Iap/Iae sprite sets）

大航海 II 有 **1v1 剑斗**（提督决斗 / 海盗船长对决），sprite 已抽出：
- 6 个玩家变种 + 1 个 NPC 模板
- 125 帧动画/角色：站姿/攻击/防御/挥剑各角度

**新游戏**：保留 1v1 决斗子系统作为情节高潮事件。

---

## 🎯 事件 / 任务系统

### 借鉴

原作通过 `Snr*.dat` 存储**剧本数据**（按文件号区分不同 chapter / scenario）。事件触发：在某时间、某地点、某状态时发生。

### 新游戏

模块化事件：
- **事件类型**：遭遇 / 发现 / 任务 / 危机 / 转折
- **触发条件**：DSL 风格，e.g.:
  ```yaml
  event: meet_pirate_king
  trigger:
    location: caribbean_sea
    after_year: 1503
    after_fame: 100
  actions:
    - dialog: pirate_king_intro
    - choice: [fight, parley, flee]
  ```

- **存储**：JSON 文件，方便修改/扩展

---

## 🎨 美术与音频

### 美术风格

- 受大航海 II 配色启发，但**全新美术**
- 选项：
  - A. 像素艺术（怀旧）—— 32×32 或 16×16 tile
  - B. 手绘像素艺术（modern pixel） —— 48×48 tile
  - C. low-poly 3D（差异化）

### 音频

- 借鉴大航海 II 的**音乐风格**（西洋古典 / 民族 BGM）
- 不直接搬运 MIDI——委托作曲或用 royalty-free 类似风格
- SE：海浪、风、船 creaking、炮声、剑击

---

## 🏗️ 技术栈建议

### 引擎选型

| 引擎 | 优势 | 劣势 |
|---|---|---|
| **Godot 4** ⭐ | 免费、2D 优、HTML5 导出、GDScript 简单 | 3D 生态偏弱 |
| Unity 6 | 生态最大、文档全 | 闭源、收费模式不稳 |
| Web Canvas / Three.js | 完全可控 | 引擎工作量大 |
| RPGMaker | 起步快 | 限制大 |

**推荐 Godot 4** + 2D 像素艺术。

### 数据驱动架构

- **所有 game data 存 JSON**：直接 import 自 Phase 1 提取（port stats / wind grid / monster stats）
- **事件用 YAML/JSON**：方便非程序员编辑
- **存档用 JSON / binary**：轻量

### 代码结构

```
/sea_demo_new/
  /assets/
    /sprites/      # 自做美术
    /audio/
    /tiles/
  /data/           # ← 从 Phase 1 JSON 直接 import
    ports.json
    ships.json
    goods.json
    wind_grid.json
    monsters.json
  /events/         # YAML 事件脚本
  /src/            # 游戏逻辑
    main.gd
    trade.gd
    naval_combat.gd
    duel.gd
    weather.gd
  /scenes/         # Godot scene 文件
```

---

## 🛣️ 实现路线图

### MVP（最小可玩版，2-3 个月）

1. 单港口贸易：买卖 5 种商品
2. 2-3 个港口可航行
3. 基础风向系统（简化为 4 方向）
4. 简单海盗遭遇（战斗用骰子模拟即可）
5. 单存档

### Beta（3-6 个月）

- 完整 20-30 个港口
- 11 种商品
- 完整风向系统（基于 Windcur.dat）
- 海战回合制系统
- 事件 / 任务系统
- 多种船只 / 升级
- 多存档

### v1.0（6-12 个月）

- 全部商品 / 港口
- 多场景 / 多主角
- 决斗系统
- 完整剧情线
- 多结局
- 翻译 / 国际化

---

## ✅ 已经从 RE 中拿到的"可直接 import"资产

| 资产 | 文件 | 用途 |
|---|---|---|
| 港口商品 stats | `output/game_data/za_dat.json` | 直接做 ports.json |
| 全球风/洋流网格 | `output/game_data/windcur_dat.json` | 直接做 wind_grid.json |
| 海怪 stats | `output/game_data/monster_dat.json` | 直接做 monsters.json |
| 港口 atlas 映射 | `output/game_data/data1_*.json` (含 Chip_no 已识别) | 港口风格分类 |
| 6 玩家决斗 sprite | `output/iap_v1/` (875 张) | 决斗动画参考 |
| NPC walking sprite | `output/char_v2/` (72 帧) | NPC 动画参考 |
| 港口 tile atlas | `output/portchip_v2/` | 港口设计参考 |
| 世界地图 | `output/contact_worldmap_v2.png` | 世界设计参考 |

---

## 🔁 与 Phase 0-2 工作的关系

```
Phase 0 (视觉资产) ────→ 美术风格参考（不直接使用）
Phase 1 (数据表)   ────→ 直接 import 作为 ports/ships/wind 平衡数据
Phase 2 (公式)     ────→ 启发性参考；新游戏可用近似公式
Phase 3 (本文档)   ────→ 把上面都综合成一份 spec
Phase 4 (实现)     ←──── 用上面的 spec 在 Godot/Unity 写代码
```

---

## 📝 Phase 3 下一步行动

1. 把 `output/game_data/*.json` 转换成新游戏可读的统一 schema
2. 选定引擎（建议 Godot 4 + GDScript）
3. 创建 MVP repo（独立于本 RE repo）
4. 第一个里程碑：**能在 2 个港口之间航行 + 买卖一种商品**

---

> Phase 3 完成。下一阶段（Phase 4）是实际写新游戏代码——属于另一个项目了。
