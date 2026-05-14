# 大航海2 反汇编笔记

> 本文件记录 `/Users/dong/Projects/Koukai2/Main.exe` 反汇编分析的进度。
> 下次开新会话从这里开始，不用从零再扫一遍。

## 1. 之前没看过的资源文件

我们之前只用了 `*.lzw` 文件，但 `/Users/dong/Projects/Koukai2/` 里还有一堆**直接可读**的事件相关文件（**不在 LS11 容器里**）：

| 文件 | 大小 | 推测内容 | 状态 |
|---|---|---|---|
| `Graph.dat` | 445 KB | **65 张事件 CG**（含 640×400 全屏图）| 结构已映射，内层压缩没解 |
| `Graph2.dat` | 78 KB | 2 张图（1 张 640×400）| 同上 |
| `Endgrp.dat` | 399 KB | **59 张结局 CG**（224×160）| 同上 |
| `Event0.dat` ~ `Event6.dat` | 8-62 KB | 事件脚本/触发表 | 未碰 |
| `1.pat` `2.pat` | 173/217 KB | 字体/tile pattern | 未碰 |
| `Hdat.put` `End_put.dat` | 31/40 KB | 不明 | 未碰 |
| `Message.dat` | 29 KB | 对话文本 | 未碰 |
| `Monster.dat` | 200 B | 海怪数据 | 未碰 |
| `Transit.dat` `Windcur.dat` `Za_dat.dat` | 各几 KB | 风/洋流/事件参数 | 未碰 |
| `D2.mml` | 28 KB | MML 格式 BGM 谱 | 未碰 |
| `Fmdrv.com` | 5 KB | FM 音源驱动 | 未碰 |
| `Snr0.dat` ~ `Snr6.dat` | 各 4-15 KB | 不明（SaNRoku？人物名册？）| 未碰 |
| `Colony.dat` | 17 KB | 殖民地数据 | 未碰 |

### `Graph.dat` / `Endgrp.dat` 结构（已确认）

外层格式跟 `Opgraph.lzw` 内部一样：

```
u32 BE offset_table[N]  # N = first_offset / 4
block_0  block_1  ...

每个 block：
  u16 LE width
  u16 LE height
  压缩位图数据
```

`Graph.dat` 解析结果：
- 65 个块，大部分 640×400（全屏 CG）
- 块 0、1 是小图（144×56 和 136×152）
- 块 2 起进入主要事件 CG，每张 20-25 KB（压缩率 ~0.16-0.20）

`Endgrp.dat`：
- 59 个块，全部 224×160
- 部分块压缩率高达 0.89 = 几乎未压缩

## 2. Main.exe MZ 头

```
offset  size  field             value
0x00    2     magic             "MZ"
0x02    2     last_page_bytes   0x0041 (65)
0x04    2     pages             0x0248 (584) → 文件总 298561 字节 ✓
0x06    2     relocs            0x146f
0x08    2     hdr_paras         0x0520 → 头大小 = 1312×16 = 20992 (0x5200)
0x14    2     init_ip           0x3374
0x16    2     init_cs           0x0000
```

代码段从文件 0x5200 开始，长 277569 字节。入口点 `cs:ip = 0:0x3374` → 文件 0x8574。

## 3. Event CG 解码器（已定位）

**入口：约 0x5e00**（文件偏移，即 EXE 文件中的位置；汇编中地址也是 0x5e00 因为 CS:IP 解释为相对 EXE 内偏移）

完整反汇编保存在 [`main_exe_decoder_disasm.txt`](main_exe_decoder_disasm.txt)。

### 函数签名（从 stack frame 推断）

调用约定：参数在 `[bp+N]`：
- `[bp+6]` = x 坐标（限 0..0x27F = 0..639）
- `[bp+8]` = y 坐标（限 0..0x18F = 0..399）
- `[bp+0xa]` = **字节读取函数指针**（far call）

返回 AX = 0xFFFF 表示参数越界错误。

### 解码流程

1. **0x5e00-0x5e3D**：参数边界检查（剪裁到 640×400 屏幕）
2. **0x5e43-0x5e52**：根据 (x, y) 计算 VRAM 起始偏移 DI（PC-9801 标准布局）
3. **0x5e54**：`call 0x5318` — 推测是 setup（清屏或 stream init？）
4. **0x5e57-0x5e5A**：`mov ax, 0xa000; mov es, ax` — **ES = 0xA000 = VRAM 段**
5. **0x5e5C-0x5e88**：从压缩流读 **16 个 LE u16**，存到 `cs:[si+0xBBC]` ——**per-image 16-entry 派发表**！这是格式的关键：每张图各自有自己的派发逻辑。
6. **0x5e89 开始**：主解码循环
   - 读 1 字节 → AL
   - `test al, 0x80` 为 0 → 跳 `[0x8a64]` 函数指针（应为结束/下一块处理）
   - `cl = al; ax = al & 0x30`（bits 4-5）
   - `test cl, 0x40` 真 → 跳 0x5F83 模式（长引用）
   - 假 → 短引用模式：
     - `shr ax, 4; inc ax` → AX = 1..4（短距离）
     - `si = di - ax`（反向引用源）
     - `cx = al & 0x0F + 1`（长度）
     - 4 路 nibble 对齐拷贝（按 si/di 奇偶分发）

### 关键 magic byte

- **`cmp al, 0x38`** at 0x6099 — 0x38 是 **escape**：读 2 字节构造 16-bit 长距离引用值（这就是为什么数据里 0x38 占 14.2%）

### nibble 对齐拷贝（0x62A0+）

经典 4bpp 像素粒度 LZ77：
```
0x6272-0x6278  shr ax, 1 ×4    ; AX = nibble_offset >> 4 = byte_offset
0x627a         inc ax
0x627b-0x627d  si = di - ax    ; back-ref source
0x627f-0x6285  shr di, 1 / rcl ax, 1 / shr si, 1 / rcl ax, 1
               ; AX 低 2 bit = di_parity << 1 | si_parity
0x6291-0x629c  按 (di_parity, si_parity) 分 4 路：
               (even, even) → 字节拷贝快路径
               (even, odd)  → nibble 拼接路径
               (odd, even)  → 镜像
               (odd, odd)   → 字节拷贝偏移 1 nibble
0x62A3-0x62EE  典型循环：lodsb / shl ×4 / and 0xF0 / or [di]&0xF / stosb
```

### VRAM 写入（0x610A 之后）

PC-9801 EGC/GDC plane select 协议：
```
mov dx, 0x3CE; mov ax, 0xF008; out dx, ax     ; ?
mov dx, 0x3C4; mov al, 2; out dx, al          ; sequencer select
inc dx; mov al, 1; out dx, al                 ; plane mask = 1
mov es:[di], bl                                ; write plane 0
shl al, 1; out dx, al                          ; plane mask = 2
mov es:[di], cl                                ; write plane 1
... 重复到 4 plane
```

所以每个"像素"实际上写 4 个 plane 字节到 VRAM。

## 4. 派发表 `cs:[bx + 0xBBC]`

16 个 u16 entries 在每张图的压缩流前面 32 字节里。**每张图不同**——这是 KOEI 的 per-image 自适应字典！

`0x6092`: `mov ax, word ptr cs:[bx + 0xbbc]` 然后 `jmp 0x610A` — 一字节命令通过 bit 4-5 索引到表中，跳转到 16 个可能的"展开"操作之一。这等价于 LS11 的 "256 字节字典"，但只有 16 个 entry（因为这里操作 nibble 而不是字节）。

## 5. 待办（继续这条路线）

### 短期（搞定 event CG 渲染）

1. **完整理解 16 模式派发表的用法** — 派发表的每个 entry 是什么？是直接的 16-bit 输出值，还是子函数偏移？看 0x6092 之后 `jmp 0x610A` 的处理流程能否解开
2. **理解长距离引用模式**（0x5F83+） — 现在只看了短距离
3. **理解 `0x5318` 子函数** — 可能是 stream reader 或 init
4. **理解 `[0x8a64]` 函数指针** — 是结束 handler 还是 chunk 切换
5. **Python 完整移植** — 估计 200-400 行代码
6. **以 `Endgrp.dat` 块 3（ratio 0.89）作为最简单测试**，能解出来再扩展

### 长期

- 反汇编 `Event*.dat` 加载器（找事件脚本格式）
- 反汇编 `Message.dat` 加载器（找文本格式）
- `1.pat`/`2.pat` 推测是字体（字符位图）—— 反汇编显示文字函数能找到

## 6. 工具状态

- **Ghidra 12.1** 装在 `/opt/homebrew/Cellar/ghidra/12.1/`，headless: `libexec/support/analyzeHeadless`
- **capstone 5.0.7** Python 包已装
- 反汇编脚本：`scripts/scan_ls11_in_exe.py`（找特定模式）

## 7. 已确认的非线索

- Main.exe 里没有 `LS11`/`LS10`/`Ls12` 字符串 → 解码器不查 magic
- 没有 `OPGRAPH` 字符串 → opgraph.lzw 是通过 wildcard `IAP*.LZW` 类似机制加载
- 字符串区在文件偏移 0x3dcf6 周围：列出所有资源文件名
