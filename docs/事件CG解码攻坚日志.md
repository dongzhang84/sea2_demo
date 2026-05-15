# 事件 CG 解码攻坚日志

> 目标：把 `Main.exe` 的事件 CG 解码器移植成 Python，解出 `Graph.dat`(65) +
> `Endgrp.dat`(59) + `Opgraph.lzw`(~14) 共约 130+ 张事件 CG。
> 全程记录在此文件。开始日期：2026-05-15。

---

## 背景与已知信息

- 源文件：`/Users/dong/Projects/Koukai2/Main.exe`（298561 字节，PC-98 16-bit MZ）
- 反汇编笔记：[`REVERSE_ENGINEERING_NOTES.md`](REVERSE_ENGINEERING_NOTES.md)
- 已有部分 disasm：[`main_exe_decoder_disasm.txt`](main_exe_decoder_disasm.txt)（0x5e00–0x63fb）
- MZ 头大小 0x5200，CS:IP 入口 0:0x3374 → 文件 0x8574。

### 解码器有两个变体（重要发现）

1. **0x5e00 变体** —— 直接写 PC-9801 VRAM（`ES=0xA000`），用 GDC/EGC plane-select
   端口（0x3CE/0x3C4）把每个像素拆成 4 个 plane 字节写出。模拟它要仿真 VRAM。
2. **0x61f4 / 0x6200 变体** —— 写普通内存缓冲区（`lodsb`/`stosb`，无 GDC OUT），
   输出是 4bpp packed 位图。**这个更适合移植**——直接拿到 bitmap。

两个变体的位流解码逻辑应当相同（同一压缩格式），只是输出端不同。

### 入口函数

- `0x61b8`：设 `[0x8a64]=0xe76`，`[0x8a62]=1`，`call 0x5dcc`，`retf`
- `0x61cc`：设 `[0x8a64]=0xe48`，`[0x8a62]=0`，`call 0x5dcc`，`retf`
- `[0x8a62]`：1=加载每图 16-entry 派发表，0=跳过
- `[0x8a64]`：命令字节 bit7=0 时跳转的 handler（0xe48 或 0xe76）

---

## 进度

### 2026-05-15 — 起步

- 读完现有 RE 笔记和 disasm。
- 确认两个解码器变体，决定优先移植 0x61f4 缓冲区变体。
- 建了反汇编工具 `scripts/disasm_exe.py`，拿到 0x61f4–0x652c 完整 disasm。

### 2026-05-15 — 解码器跑通（核心突破）

- 决定**不手工移植**那段 nibble 对齐 LZ 汇编（太绕、易错），改用
  **unicorn 16-bit x86 模拟器直接跑原始机器码**。
- `scripts/decode_eventcg.py`：把 Main.exe 代码段载入模拟器，按
  far-call 约定铺栈，跑 0x61f4 解码器函数。
  - 函数参数：`[bp+6]`=输入段，`[bp+8]`=输入偏移，`[bp+0xa]`=输出段。
  - 函数自包含，只调用 0x61df（单字节读取器），无端口 I/O。
- **一次跑通**：Endgrp.dat block 3 返回 AX=0（成功），写出 17920 字节。
- 像素格式破解：**4bpp planar，字节交错**——每 8 像素列有连续 4 字节
  （4 个 plane）。`pixel(x,y) = Σ bit(7-x%8) of out[(y·W/8+x//8)·4+p] << p`。
- **Endgrp.dat 57/59 张解码成功**，形状完全正确（剩 2 张是 640×400）。

**未解决**：
1. 真实调色板未找到（当前用占位 16 色，颜色不对）。
2. 640×400 大图：0x61f4 解码器 DI 是 16 位，>64KB 会溢出 —— 大图需要
   改用 0x5e00 VRAM 解码器变体。

### 2026-05-15 — VRAM 解码器跑通，全部事件 CG 解出

- `scripts/decode_eventcg_vram.py`：模拟 0x5e00 VRAM 解码器变体。
  - 实现了 VGA write-mode-0 模型：拦截 sequencer(0x3C4/5) / GC(0x3CE/F) 端口，
    维护 4 个 plane 缓冲 + latch + map-mask + bit-mask + data-rotate。
  - 字节读取器：拦截 `lcall [bp+0xa]` (机器码 ff5e0a) 直接喂输入字节。
  - 图在 VGA 帧里固定 640 宽、垂直居中 (基址偏移 0xc80 = 40 行)。
- **关键发现**：事件 CG 有两种编码模式 ——
  - 带表模式 (入口 0x61b8)：每图带 16-entry 派发表。
  - 无表模式 (入口 0x61cc)：无派发表。
  - 同一文件里两种都有！判据：正确解码 ⟺ VGA 写入数 == w×h。
  - `decode_auto()` 两种模式都试, 自动选对的。
- **全部解出**：
  - `Endgrp.dat`  59/59 张
  - `Graph.dat`   65/65 张
  - `Opgraph.lzw` 107 张 (先 LS11 解压成 14 part, 每 part 是「偏移表+多块」容器)
  - **合计 231 张事件 CG** —— 攻坚目标达成 (原估 ~130 张)。

**唯一未解决**：真实 16 色调色板 (现用占位灰度, 形状全对)。

### 2026-05-15 — 调色板调查

确认了**调色板不在图像块里**：
- 几乎所有 block 都把输入消耗到底（无尾部数据）。
- 16-entry 派发表不是调色板（后 8 项的值不符合 `0x0GRB` 格式，且确认被解码器当字典用）。

调色板由可执行文件加载。在 Main.exe / End.exe / Open.exe 都找到 VGA DAC
调色板例程：
- `0x679b set_palette(start, count, src_off)` —— 从 DS:SI 批量载入 N 色，每色 3 字节 RGB。
- `0x680a set_one(index, 0x0GRB_word)` —— 单色，16-bit `0x0GRB` 格式。
- `0x9071` —— 回读 DAC。

但这些例程是经**间接派发**调用的（KOEI 引擎用 `INT 66h` 做 syscall 分发），
没有直接 far call，静态追踪调色板数据源很深。

**结论**：解码器攻坚目标已完成（231 张 CG 全解出）。要拿到**原汁原味的
调色板**，需要更深的工作——要么追完 INT 66h 派发链，要么用模拟器跑
Open.exe / End.exe 的确定性开场/结局序列、在它显示 CG 时抓 DAC 调色板。
鉴于本项目「美术全新自做、原作只做参考」，灰度提取已可作内容参考。

### 攻坚状态：核心目标达成
- ✅ 事件 CG 解码器移植成功，231 张 CG 全解出。
- 🟡 真实调色板待后续（外部、间接派发，需更深 RE 或动态模拟）。
