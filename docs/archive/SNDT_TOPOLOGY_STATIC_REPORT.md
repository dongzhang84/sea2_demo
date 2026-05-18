# SNDT 静态拓扑报告

> 这是第一版“静态拓扑下限”报告。它不声称已经反编译 SNDT VM，
> 只整理当前确定能从文件结构直接得到的拓扑事实，并把不确定的文本引用明确标成噪声候选。

相关产物：

- `output/sndt_topology/sndt_topology.json`
- `output/sndt_topology/sndt_topology.dot`
- `output/sndt_topology/sndt_text_refs.md`
- 生成脚本：`scripts/export_sndt_topology.py`

---

## 1. 已经能确定的结构

`Snr0.dat` 到 `Snr6.dat` 都是 SNDT 剧本脚本文件。当前能稳定解析到：

```text
SNDT file
  -> chunk
    -> subscript
      -> dispatch table
      -> bytecode area
```

其中：

- chunk 是较大的剧情/任务块。
- subscript 是 chunk 内的分支或子流程。
- 每个 subscript 开头通常有一张 dispatch table。
- dispatch table 由 `(key, target)` 组成。
- `key` 可拆成：
  - 高字节 `tag`
  - 低字节 `selector`
- `target` 是 subscript 内偏移，代表该 key 命中时跳到的位置。

这些边界和派发表边属于结构事实，不依赖 opcode 语义。

---

## 2. 汇总统计

| 文件 | chunk | subscript | dispatch edge | 原始文本引用候选 | `.mes` 文本数 |
|---|---:|---:|---:|---:|---:|
| `Snr0` | 13 | 35 | 42 | 770 | 192 |
| `Snr1` | 6 | 40 | 152 | 142 | 1176 |
| `Snr2` | 8 | 46 | 161 | 93 | 917 |
| `Snr3` | 6 | 25 | 83 | 92 | 532 |
| `Snr4` | 5 | 10 | 28 | 33 | 234 |
| `Snr5` | 4 | 11 | 53 | 65 | 326 |
| `Snr6` | 6 | 19 | 226 | 207 | 926 |
| **合计** | **48** | **186** | **745** | **1402** | **4303** |

解释：

- `dispatch edge` 是确定结构边。
- `原始文本引用候选` 来自 bytecode 区里的裸扫 `0x0c XX`。
- 因为 opcode 长度表还没恢复，文本引用候选里有假阳性。

---

## 3. 当前已经看到的拓扑形态

### `Snr0`：通用任务系统

`Snr0` 明显不是某个单独主人公主线，而是通用任务/委托系统。

静态结果支持之前日志里的判断：

- `Snr0.chunk0` 是任务入口密集区。
- 文本候选集中出现：
  - 运货任务
  - 采购任务
  - 剿海盗任务
  - 超时/继续/完成/报酬分支
- `Snr0.chunk6` 到 `Snr0.chunk12` 呈现重复模板结构。

这说明 `Snr0` 很可能是“任务模板 + 多种实例”的系统脚本。

### `Snr1-6`：六个主人公脚本

`Snr1` 到 `Snr6` 的结构更像主人公主线：

- chunk 数较少，通常 4 到 8 个。
- dispatch edge 数量差异明显，说明不同主人公的剧情复杂度不同。
- `Snr6` 只有 19 个 subscript，但有 226 条 dispatch edge，说明它存在较密集的状态派发表。
- `Snr4` 只有 10 个 subscript、28 条 edge，是目前静态结构最小的一条线，适合作为后续 opcode 实验对象。

---

## 4. 文本引用的置信度

当前报告和 JSON 里所有 `0x0c XX` 文本引用都标为：

```text
confidence = noisy
```

原因：

- 已确认 `0x0c` 是显示文本 opcode。
- 但还没有 opcode 长度表。
- 裸扫 bytecode 时，某些其他 opcode 的操作数字节也可能刚好等于 `0x0c`。
- 所以 raw scan 会混入假文本引用。

这不是失败，而是当前阶段应有的保守标注。

下一步一旦恢复 opcode 长度表，文本引用可以升级为：

```text
confirmed
```

并且能沿真实控制流排序。

---

## 5. 这份静态拓扑已经解决了什么

它解决的是“现在到底站在哪里”：

- 已把 7 个 SNDT 文件统一导出成 JSON。
- 已把 chunk/subscript/dispatch edge 变成可机器处理的数据。
- 已把文本引用候选集中到一个 Markdown 报告。
- 已生成 Graphviz DOT，可继续转成图。
- 已经可以选择更具体的下一步攻击目标。

这一步把散落在日志里的结构发现变成了可审阅产物。

---

## 6. 仍未解决的问题

未解决的问题仍然是 SNDT VM 本身：

- opcode 长度未知。
- opcode 语义未知。
- 条件分支 opcode 未定位。
- flag / 变量读写未命名。
- 事件入口和解释器循环未定位。
- 当前 DOT 里的派发表目标还是 offset 节点，还没全部解析成真实 basic block。

换句话说：现在有了“容器拓扑”和“派发表边”，还没有完整“执行拓扑”。

---

## 7. 下一步建议

下一步不应继续扩大裸扫，而应转向两个方向之一。

### 路线 A：自动化动态追踪

目标：

- 找到 Main.exe 里逐字节执行 SNDT bytecode 的解释器循环。
- 观察 bytecode 指针处理 `0x0c` 和 `0xf2` 时如何前进。
- 恢复 opcode 长度。

第一版脚本：

```text
scripts/sndt_trace_runner.py
```

它应该封装现有 `scripts/dbg_driver.py`，自动下断点、dump 寄存器、保存调试日志。

### 路线 B：选择最小静态目标

目标：

- 先不全破 7 个文件。
- 选一个最小、结构简单的对象做 opcode 实验。

候选：

- `Snr4`：结构最小，适合先做。
- `Snr0.chunk0`：文本密集，适合验证任务模板。
- `Snr1` 开场：剧情价值高，但可能需要更多运行时状态。

我的建议：

```text
先用 Snr4 做 opcode 长度实验，再回到 Snr0 任务模板。
```

理由：

- `Snr4` 结构小，调试面更窄。
- `Snr0` 文本和任务逻辑最丰富，适合在长度表初步恢复后验证。

---

## 8. 当前阶段结论

Claude Code 之前留下的是“结构发现 + 调试基础设施”，但没有形成拓扑产物。

本阶段已经补上第一层产物：

```text
静态拓扑下限 = SNDT 容器结构 + 派发表边 + 文本引用候选
```

下一阶段要做的不是让用户手动玩游戏，而是写自动化追踪器，或者构造最小 SNDT 实验样本。

