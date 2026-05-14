# Phase 2: Main.exe RE — 进度笔记

> 目标：从 Main.exe 提取核心游戏公式（贸易/海战/风向/事件）。
> 状态：基础设施已映射，深度公式提取需更多工作。

## ✅ 已搞清楚

### Main.exe 关键结构

| 项目 | 位置 | 备注 |
|---|---|---|
| MZ header size | 0x5200 | 代码从此起 |
| Entry point | file 0x8574 (cs:ip=0:0x3374) | |
| 5 个 segment 值 | 0x0000, 0x0fea, 0x1fd9, 0x2e09, 0x3815 | |
| 字符串段 | seg 0x3815 (base 0x3d350) | 含所有文件名 + 错误消息 |
| **文件开 wrapper** | **0x521c (CS:IP = 0:0x1c)** | DOS INT 21h AH=3D 通用包装 |
| 消息显示函数 | 0x27f62 | 处理 byte 流 + control byte |
| 事件 CG 解码器 | 0x5e00 | 详见 REVERSE_ENGINEERING_NOTES.md |

### 文件开调用点（6 个 far call 到 0:0x1c）

| Call site | 推送的文件名 offset | 文件 |
|---|---|---|
| 0x1b3b1 | 0xa25c | **1.pat** (字体 1) |
| 0x1b3d8 | 0xa269 | **2.pat** (字体 2) |
| 0x1c103 | 0xa9c | **C:KOUKAI2.DAT** |
| 0x1c171 | 0xa9c | C:KOUKAI2.DAT (不同模式?) |
| 0x1c2f3 | 0xa9c | C:KOUKAI2.DAT (再次) |
| 0x1b1bd | (失败处理) | error path |

### 🔑 KOUKAI2.DAT — 主数据文件

- **328,991 字节** ≈ 321 KB（之前完全没注意到！）
- 开头是 **16 字节 / record** 的"情景启动菜单"：
  - 12 字节 ASCII 日期 ("DD/MM/YYYY" 格式)
  - 4 字节元数据（player char ID + flags）
- 多个起始日期 1501 / 1525 / 1526 / 1527——对应**多个可选场景 / 主角**
- 之后是 game-data 块（船舶/人物/物品 stats？需深挖）

**这个文件可能包含 Za_dat / Colony / Monster 等小 .dat 之外的更多 game data。** 标准 .dat 文件可能是模块化拆分，KOUKAI2.DAT 是 fallback 或完整数据。

### 文件名字符串清单（来自 Main.exe 段 0x3815）

```
COLONY.DAT  WINDCUR.DAT  ZA_DAT.DAT  MONSTER.DAT  TRANSIT.DAT
HDAT.PUT    SNRDAT.LZW   SNRMES.LZW  DATA2.LZW    EVENT.LZW
IKKI.LZW    KAO.LZW      PORTCHIP.LZW  WORLDMAP.LZW  PORTMAP.LZW
IAP*.LZW    IAE1.LZW     CHAR.LZW     DATA1.LZW    KOUKAI2.DAT
1.pat       2.pat        ITEM.MES     SNR*.MES     CHIP_NO.DAT
NAME.TBL    USERNAME.DAT D2.MML
```

注：**所有这些名字都在 Main.exe**，但只有 KOUKAI2.DAT, 1.pat, 2.pat 实际通过 0x521c wrapper 加载。其他文件可能：
- 通过别的代码路径加载（待发现）
- 仅在错误消息中被引用
- 由 Open.exe / End.exe 加载

---

## 🟡 仍未搞定（需更深 Ghidra 时间）

1. **价格波动公式**——核心玩法。需找到处理 Za_dat.dat 数据的函数
2. **海战伤害公式**——需找战斗子系统入口
3. **风向影响速度公式**——结合 Windcur.dat 30×45 网格
4. **事件触发条件**——需找事件 VM 解释器
5. **NPC 忠诚度算法**——舰队管理核心

---

## 📋 用什么方法可以继续推进 Phase 2

### 路径 A: 启动 Ghidra GUI，做完整 auto-analysis（推荐）
- 一次性 import + 跑完所有 analyzers (30 分钟)
- 然后 GUI 浏览 calls graph，找数据库的引用
- 工具效率高 10×

### 路径 B: 继续 capstone CLI 手挖
- 写脚本顺着函数调用图爬
- 启动门槛低但效率低
- 一次只能盯一个细节

### 路径 C: DOSBox 跑游戏 + 内存观察
- 让游戏自己跑，从内存中扒数据
- 间接但能 100% 验证
- 需 PC-98 模拟器（np2/Anex86）

### 路径 D: 仅靠数据 + 经验逆向公式
- 已有的 Za_dat / Windcur 已经够多
- 直接根据数据 PATTERN 猜公式（"价格 = 基础值 × (1 + 浮动)") 
- 大航海 II 的机制经典公开，可参考社区文档

**实际建议**：Phase 2 的"完整公式提取"对单人项目来说**ROI 偏低**。

更好的策略：
1. **当作 Phase 3 设计文档的"经验型"输入** —— 用现有数据 + 大航海 II 的公开机制描述 推导一个**"合理近似"** 的新游戏公式
2. **新游戏不必复刻原作公式** —— 抓"核心 vibe"就行（价格根据需求/供给+随机扰动；海战考虑风向角度等）
3. **Phase 2 重点转向**：仅在需要某个具体细节（"金币计算"、"探险成功率"）时再做针对性 RE

---

## 📊 5 阶段进度更新

```
✅ Phase 0: 视觉资产                90%+
✅ Phase 1: 数据表                  ~80% (raw 已抽完, semantic 待补)
🟡 Phase 2: Main.exe RE             ~15% (基础设施 + KOUKAI2.DAT 发现)
⬜ Phase 3: 设计文档                0% (下一步可启动)
⬜ Phase 4: 现代实现                0%
```

**当前推荐**：直接进入 **Phase 3 = 写设计文档**。基于已有数据 + 经典大航海机制知识，把新游戏的 spec 写出来。Phase 2 的深度公式提取可以**在 Phase 4 实现时遇到具体需求再回来挖**。
