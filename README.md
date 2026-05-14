# sea2_demo — 大航海時代II 资源逆向

KOEI《大航海時代II》(Uncharted Waters II, 1993, PC-9801) 的资源文件逆向。

目前进度：成功从 `Kao.lzw` 提取出全部 128 张人物头像。

![128 portraits](output/contact_kao_v4.png)

## 结果

- **源文件**：`/Users/dong/Projects/Koukai2/Kao.lzw` (155 KB, LS11 压缩)
- **解压后**：256 个 part — 前 128 个各 1920 字节（全身头像），后 128 个各 864 字节（待定）
- **渲染**：80×64 像素，8 色调色板，3-plane 编码
- **输出**：`output/kao_png_v4/000.png` ~ `127.png` + 整版 `output/contact_kao_v4.png`

## 跑一遍

```bash
# 1. 解压 Kao.lzw → 256 个 part 文件
python3 scripts/ls11_decode.py /Users/dong/Projects/Koukai2/Kao.lzw output/kao_parts

# 2. 渲染 128 张头像 PNG + 整版 contact sheet
python3 scripts/render_kao_v4.py
```

依赖：`pip install Pillow numpy`

## 目录结构

```
scripts/
  ls11_decode.py      — LS11 / Ls12 解压器（KOEI 自定义变长前缀码）
  render_kao_v4.py    — 80×64 / 8色 / 3-plane 头像渲染
  experiments/        — 失败的尝试（保留作记录，见 CLAUDE.md）

output/
  kao_parts/          — 解压出的 256 个原始 part
  kao_png_v4/         — 128 张头像 PNG
  contact_kao_v4.png  — 整版预览
```

## 技术要点

**LS11 压缩格式**（`scripts/ls11_decode.py`）：
- Magic `"LS11"` 或 `"Ls12"`，文件头 16 字节
- 256 字节自定义字典（每个文件独立）
- 12 字节大端 index 记录：`(compressed_size, uncompressed_size, offset)`
- 变长前缀码位流：读 bit 直到遇到 0 → 得到 `mask_len`；再读 `mask_len` bits = `factor`；`code = (2^mask_len - 2) + factor`
- `code < 256`：输出 `dictionary[code]`
- `code >= 256`：回溯复制 `code - 256` 字节，长度为下一个 code + 3

**头像位图格式**（`scripts/render_kao_v4.py`，源自 JohanLi 的研究）：
- 每张头像 1920 字节 = 15,360 bits
- 80 行 × 64 列像素，分成 640 个 8 像素块
- 每个 8 像素块占 24 bits（3 个 plane × 8 bits）
- 像素 `j` 的颜色索引 = `bits[p+j]<<2 | bits[p+j+8]<<1 | bits[p+j+16]`，pointer 每块 +24

固定 8 色调色板（黑/绿/橙/肤/蓝/天蓝/粉/米白）。

## 参考

- [tzengyuxio/kaodata](https://github.com/tzengyuxio/kaodata) — LS11 解压算法
- [JohanLi/uncharted-waters-2-research](https://github.com/JohanLi/uncharted-waters-2-research) — 大航海II 头像位图格式

## 还没碰的文件

`Koukai2/` 里其他 `.lzw` 都是 LS11 同一格式，估计 `ls11_decode.py` 都能解压，只是位图编码可能不同：

`Char.lzw` `Data1.lzw` `Iae1.lzw` `Iap1-6.lzw` `Opgraph.lzw` `Portchip.lzw` `Portmap.lzw` `Worldmap.lzw`
