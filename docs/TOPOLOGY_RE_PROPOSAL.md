# 大航海 II 游戏拓扑逆向 Proposal

> 目标：接着现有 Claude Code 工作，把项目从“资源/文本/原型游戏”重新拉回到
> **游戏结构逻辑逆向**。这里的“拓扑”指：6 个主人公在什么状态、时间、地点、flag
> 下触发什么事件，事件内部如何分支，显示哪些文本，修改哪些变量，最终流向哪里。

---

## 1. 当前判断

Claude Code 已经做了不少基础工作，但真正目标还没完成。

它完成较好的部分：

- 资源逆向：头像、道具、港口图、世界地图、船图、NPC sprite 等基本已解。
- 文本逆向：`Message.dat`、`Snr*.mes` 大量文本已经能读。
- SNDT 容器结构：`Snr0-6.dat` 已解析到 `文件 -> chunk -> 子脚本 -> 派发表 -> 字节码`。
- 已确认少量 opcode：
  - `0x0c` = 显示文本，后跟 1 字节文本索引。
  - `0xf2` = 子脚本结束。
- 动态调试基础设施：
  - `game_dos/` 可启动。
  - `scripts/dbg_driver.py` 可控制 DOSBox-X debugger。
  - `scripts/ls11_encode.py` 可重建 `SNRDAT.LZW` / `SNRMES.LZW`。

但它没有完成的关键部分：

- 没有找到 SNDT 字节码解释器主循环。
- 没有恢复 opcode 长度表。
- 没有恢复 opcode 语义。
- 没有生成“事件拓扑图”或“剧情/任务结构图”。
- 没有把动态追踪变成可重复实验，最后变成“用户手动玩，AI 监控”。

结论：**Claude Code 现在停在了 SNDT VM 入口前。结构层已摸到，拓扑层没有真正落地。**

---

## 2. 关键卡点

核心卡点不是图片、文本或 Godot，而是：

```text
Snr0-6.dat 里的 SNDT bytecode VM 未破
```

目前我们能知道一个子脚本在哪里开始、在哪里结束，也能裸扫出部分 `0x0c` 文本引用。
但因为 opcode 是变长的，裸扫会扫进其他指令的操作数字节，造成假文本、假分支、假结构。

所以必须解决至少一个问题：

```text
如何按真实指令边界遍历 SNDT bytecode？
```

要做到这个，有两条路：

- 找到 Main.exe 里的解释器循环，从运行时观察 opcode 指针怎么移动。
- 或者通过静态约束和统计优化恢复足够可信的 opcode 长度表。

Claude Code 试过简单静态约束，失败是合理的：只要求“能平铺到 f2”会退化成每个字节都是 1 字节指令，约束太弱。

---

## 3. 我建议的交付物

接下来不应该继续泛泛“研究”，而应该做成几个明确产物。

### 交付物 A：静态拓扑下限

文件：

```text
output/sndt_topology/sndt_topology.json
output/sndt_topology/sndt_topology.dot
output/sndt_topology/sndt_text_refs.md
```

内容：

- 每个 `Snr*.dat` 的 chunk / subscript / dispatch table。
- 每个子脚本已知派发表边：`key -> target offset`。
- 每个子脚本里可信度分级的文本引用：
  - confirmed：按已知边界或强模式确认。
  - probable：上下文看起来合理。
  - noisy：裸扫得到，可能是假阳性。
- 每个 chunk 关联的 `.mes` 文本片段摘要。

目的：

即使 VM 没完全破，也先给出一张“已知结构地图”。这不是最终拓扑，但能让人看到已经站在哪里。

### 交付物 B：自动化动态追踪 runner

文件：

```text
scripts/sndt_trace_runner.py
output/sndt_trace/session_*.log
output/sndt_trace/memdump_*.bin
```

功能：

- 启动或连接 `dbg_driver.py`。
- 自动发调试器命令。
- 自动设置断点，例如：
  - `19b4:b81a`：已定位的事件触发检查函数。
  - 疑似 `0000:8ebc`：可能的事件脚本入口。
- 自动 dump 寄存器、调用栈、关键内存段。
- 不要求用户手动玩游戏。

如果必须进入某个画面，也应该脚本化按键流程，而不是让用户操作。

### 交付物 C：最小 SNDT 实验样本

文件：

```text
output/sndt_lab/minimal_snr*.dat
output/sndt_lab/patch_notes.md
```

思路：

- 不直接挑战完整剧情。
- 构造或 patch 一个最小脚本，只包含少量已知模式：
  - 显示文本 `0x0c`
  - 结束 `0xf2`
  - 一个分支或变量检查
- 重建 `SNRDAT.LZW` 后让游戏加载。

目的：

把“复杂剧情触发”降成可重复的实验。每次只观察一个 opcode 或一小段指令。

### 交付物 D：opcode 长度/语义表

文件：

```text
docs/SNDT_OPCODE_TABLE.md
output/sndt_topology/opcodes.json
```

内容示例：

```text
0x0c len=2  show_text(text_id)
0xf2 len=1  return/end
0xc0 len=?  probable condition/setup
0xc7 len=?  probable separator/end-block
0xc8 len=?  probable index/event op
0xcc len=?  probable compare/load immediate
```

目标不是一次性全破，而是逐步把 opcode 从 unknown 变成 length-known，再变成 semantic-known。

---

## 4. 执行计划

### Phase 1：整理现有事实，产出静态拓扑下限

目标：不依赖 DOSBox，不依赖手玩，先把已有结构变成可审阅产物。

步骤：

1. 扩展 `scripts/analyze_sndt.py`，新增 JSON 输出。
2. 给每个 chunk / subscript 分配稳定 ID：
   - `Snr1.chunk0.sub3`
   - `Snr0.chunk6.sub1`
3. 导出派发表边。
4. 在码区内扫描 `0x0c` 文本引用，但标注置信度。
5. 生成 Graphviz `.dot`，把 chunk / subscript / dispatch target 画出来。

完成标准：

- 能打开一个 JSON 看见 7 个 SNDT 文件的结构。
- 能打开 `.dot` 看到每个主人公脚本的骨架。
- 能在 markdown 里看到每个子脚本可能显示的文本。

风险：

- 文本引用会有噪声，因为 opcode 长度表未恢复。

应对：

- 不伪装成最终结果，明确标注 `confirmed/probable/noisy`。

### Phase 2：自动化动态追踪

目标：替代“用户手动玩游戏”。

步骤：

1. 写 `scripts/sndt_trace_runner.py`，封装 `/tmp/dbg_cmd` 和 `/tmp/dbg_screen.txt`。
2. 自动启动 DOSBox-X 或连接已有 `dbg_driver.py`。
3. 自动下断点：
   - `19b4:b81a`
   - `0000:8ebc`
   - 其他从调用栈推导出的候选地址。
4. 自动记录每次命中时：
   - CS:IP
   - AX/BX/CX/DX/SI/DI/DS/ES/SS/SP/BP
   - 栈窗口
   - 当前反汇编窗口
   - 若可行，dump 相关段内存。
5. 如果按键流程稳定，再把“新游戏 -> 选 João -> 进酒馆剧情”也脚本化。

完成标准：

- 用户不需要操作游戏。
- runner 能重复跑到同一个断点或同一类事件检查点。
- 每次运行留下结构化 log。

风险：

- DOSBox-X debugger 命令格式不稳定。
- 游戏输入自动化可能受画面状态影响。

应对：

- 第一版不追求完整自动通关，只自动化 debugger 层。
- 游戏层输入若不稳定，改走 patch / forced-call 路线。

### Phase 3：最小实验脚本 / patch 路线

目标：不依赖真实剧情触发，主动制造 SNDT 执行场景。

步骤：

1. 选一个最短、最容易观察的 `Snr0` 子脚本。
2. 构造或 patch 其代码区，使它只执行：

   ```text
   0c XX
   f2
   ```

3. 用 `ls11_encode.py` 重建 `SNRDAT.LZW`。
4. 让游戏进入会调用该脚本的位置。
5. 观察解释器执行这两个 opcode 的路径。
6. 逐步增加一个未知 opcode，恢复长度和语义。

完成标准：

- 能稳定证明 `0x0c` 在解释器中的处理函数在哪里。
- 能看到 bytecode 指针从 `0x0c` 前进到下一条指令。
- 能用同一方法测量其他高频 opcode。

风险：

- 游戏可能校验或依赖脚本上下文。
- 最小脚本可能缺少必要前置状态。

应对：

- 先 patch 已会执行的真实脚本，不凭空新增。
- 保留原 chunk/subscript 外壳，只替换局部 bytecode。

### Phase 4：生成第一版机器拓扑

目标：把“opcode 长度表 + 文本引用 + 派发表”合并成真正可用的拓扑图。

步骤：

1. 用已恢复长度表写一个 `sndt_disasm.py`。
2. 对所有 `Snr*.dat` 做线性反汇编。
3. 识别：
   - 文本显示
   - 条件分支
   - 变量读写
   - 事件跳转
   - 结束
4. 生成：

   ```text
   output/sndt_topology/topology_v1.json
   output/sndt_topology/topology_v1.dot
   docs/SNDT_TOPOLOGY_REPORT.md
   ```

完成标准：

- 至少能完整还原 `Snr0` 通用任务系统的一条任务模板。
- 至少能还原 `Snr1` 主人公開场剧情的一段真实分支。

---

## 5. 不再做的事

为了不偏离目标，以下事项暂时不做：

- 不继续打磨 Godot 游戏。
- 不继续解事件 CG 图片。
- 不继续做美术替换。
- 不继续泛化“新游戏设计文档”。
- 不让用户手动玩游戏来触发事件。

这些不是没价值，而是和“游戏拓扑逆向”目标不在同一条线上。

---

## 6. 我对当前 repo 的接手判断

这个项目不是从零开始。Claude Code 留下的基础设施有用，尤其是：

- SNDT 容器解析。
- 文本解码。
- DOSBox-X 调试桥。
- 重建 LZW 能力。

但接下来必须改变工作方式：

```text
从“边玩边看”改成“可重复实验 + 可审阅产物”。
```

第一步我建议先做 **静态拓扑下限**。它不会解决全部 VM，但能立刻把已有成果变成你能看的东西。
第二步再做 **自动化动态追踪**，目标是破 opcode 长度表。

如果只选一个最短可交付，我会先做：

```text
scripts/export_sndt_topology.py
output/sndt_topology/sndt_topology.json
output/sndt_topology/sndt_topology.dot
docs/SNDT_TOPOLOGY_STATIC_REPORT.md
```

这会把“已经做到哪里”从散落的日志，变成一份实际拓扑草图。

