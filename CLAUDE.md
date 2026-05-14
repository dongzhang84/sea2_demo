# CLAUDE.md

Context for future Claude sessions in this repo. Read this before suggesting changes.

## What this repo is

逆向《大航海時代II》(KOEI, 1993, PC-9801) 资源文件。源文件不在 git 里——本地路径 `/Users/dong/Projects/Koukai2/`。

**当前状态**：`Kao.lzw` 的 128 张头像已成功解出。其他 `.lzw` 文件未处理。这不是要做 demo——纯粹的资源逆向。

## What worked (canonical pipeline)

1. `scripts/ls11_decode.py <file.lzw> <out_dir>` — KOEI LS11 解压（算法来自 tzengyuxio/kaodata）
2. `scripts/render_kao_v4.py` — 80×64 / 8色 / 3-plane 头像渲染（算法来自 JohanLi/uncharted-waters-2-research）

两步组合 → `output/contact_kao_v4.png` 是验证成功的最终输出。

## What did NOT work (don't redo)

`scripts/experiments/` 里的全部尝试都试过且失败了。简记：

| 文件 | 假设 | 为什么错 |
|---|---|---|
| `decode_lzw.py` | 标准 LZW 变长码 | KOEI 用的是变长前缀码 + 自定义字典，不是 LZW |
| `decode_ls11.py` | 字节对齐 LZSS (6 种参数组合) | LS11 不是 LZSS，是位流前缀码 |
| `decode_bitlzss.py` | 位对齐 LZSS (144 种参数组合) | 同上，算法根本不是 LZSS 系列 |
| `render_kao.py` (v1) | 4-plane 16色 planar (PC-9801 典型) | 实际是 3-plane 8色，stride 也不同 |
| `render_kao_v2.py` | 6 种 chunky 4bpp 变体 | 同上 |
| `render_kao_v3.py` | 把 part 内部拆/或 part[i]+part[i+128] 拼一起 | 后 128 个 part 是别的东西（864 字节，可能是物品/小图标），不是头像的另一半 |

**根本经验**：盲试参数浪费大量时间。先 GitHub 搜「<file ext> format」、找现成解码器（tzengyuxio, JohanLi 这类），比对位流细节快几十倍。

## Format spec (verified)

### LS11 / Ls12 压缩

```
bytes 0-3    : magic "LS11" 或 "Ls12"
bytes 4-15   : reserved (零)
bytes 16-271 : 256 字节自定义字典（每文件独立！）
bytes 272+   : 12 字节大端 index 记录:
               (compressed_size: u32, uncompressed_size: u32, offset: u32)
               以 4 个零字节结束
data area    : 压缩 part 数据，offset 是绝对偏移
```

位流解码（大端，MSB first）：
- 读 bit 直到遇到 0 → `mask_len` = 读了几个 bit
- 再读 `mask_len` bits → `factor`
- `code = (2^mask_len - 2) + factor`
- 若 `code < 256` → 输出 `dictionary[code]`
- 若 `code >= 256` → 设 `delta = code - 256`；下一个 code 解码出的值 `+3` 作为长度，从当前输出回退 `delta` 字节复制

### Kao.lzw 头像位图

- 解压出 256 个 part：前 128 个 = 1920 字节（头像），后 128 个 = 864 字节（未知）
- 1920 字节 = 15,360 bits → unpackbits 成 bit 数组
- 80 行 × 64 列 = 640 个「8 像素块」
- 每块占 24 bits：`bits[p..p+8]` 是 plane 0，`bits[p+8..p+16]` 是 plane 1，`bits[p+16..p+24]` 是 plane 2
- 像素 j (0..7) 的颜色索引 = `(plane0[j]<<2) | (plane1[j]<<1) | plane2[j]`
- pointer `+= 24` 进下一块

调色板（来自 JohanLi）：
```
0=#000000 1=#00A060 2=#D04000 3=#F0A060
4=#0040D0 5=#00A0F0 6=#D060A0 7=#F0E0D0
```

## 还能做什么

1. **后 128 个 part (864 字节)** — 没解码。可能是小尺寸物品图、商品图标，或船只缩略图。864 = 16×27×2 / 也可能 = 24×24×... 试 JohanLi repo 里其他位图格式。
2. **其他 `.lzw`** — `Koukai2/` 里 14 个 `.lzw` 文件都是 LS11 格式（用 `ls11_decode.py` 都能解压），但各自位图编码不同：
   - `Worldmap.lzw` / `Portmap.lzw` — 地图，估计是 tile 索引 + tile 集合
   - `Char.lzw` — 字符字库
   - `Portchip.lzw` — 港口建筑 chip
   - `Iap1-6.lzw` `Iae1.lzw` — 不明
   - `Data1.lzw` — 数据表，不是图
3. **应用到 San4** — 三国志IV 的 `MAINMAP.S4` 据说也是 LS11 magic，可以试同一个解码器。

## 项目约定

- 脚本路径都用 `Path(__file__).resolve().parent.parent` 做 repo-relative，不要写绝对路径。
- `output/` 全部由脚本生成，不在 git 里。
- `experiments/` 是历史记录，不要删，但也不要再加新的失败尝试（直接改 v4 / 新加 v5 即可）。
- 用户偏好简短回复，看图说话——渲染完直接 Read 出 PNG 给他看。
