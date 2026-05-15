#!/usr/bin/env python3
"""事件 CG 解码器 —— 用 unicorn 直接跑 Main.exe 里的缓冲区解码器 (0x61f4)。

绕过手工移植那段绕人的 nibble 对齐 LZ 汇编：直接在 16-bit x86 模拟器里
执行原始机器码。输入 = Graph.dat/Endgrp.dat 的一个 block，输出 = 解码后的
位图缓冲区。

地址约定：Main.exe MZ 头 0x5200，cs=0 → file 0x5200。
解码器函数 file 0x61f4 = cs-offset 0xff4。
"""
import struct
import sys
from pathlib import Path

from unicorn import (Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_MEM_WRITE,
                     UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_SS, UC_X86_REG_SP,
                               UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_DI,
                               UC_X86_REG_IP, UC_X86_REG_AX)

EXE = Path("/Users/dong/Projects/Koukai2/Main.exe")
SEG_BASE = 0x5200            # file offset of cs:0
DECODER_FOFF = 0x61f4        # file offset of the buffer decoder
DECODER_IP = DECODER_FOFF - SEG_BASE   # 0xff4

# memory layout (linear)
CODE_LIN = 0x10000; CODE_SEG = 0x1000; CODE_LEN = 0x2000
STACK_LIN = 0x30000; STACK_SEG = 0x3000
OUT_LIN = 0x40000;  OUT_SEG = 0x4000;  OUT_LEN = 0x40000
IN_LIN = 0x90000;   IN_SEG = 0x9000;   IN_LEN = 0x10000
RET_LIN = 0xF0000

_exe = EXE.read_bytes()


def decode_block(block: bytes, trace: bool = False):
    """Run the decoder on one block. Returns (out_bytes, di_end, width, height)."""
    width, height = struct.unpack_from("<HH", block, 0)

    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    uc.mem_map(CODE_LIN, CODE_LEN)
    uc.mem_map(STACK_LIN, 0x1000)
    uc.mem_map(OUT_LIN, OUT_LEN)
    uc.mem_map(IN_LIN, IN_LEN)
    uc.mem_map(RET_LIN, 0x1000)

    # load code segment (file 0x5200 .. ) at cs linear
    uc.mem_write(CODE_LIN, _exe[SEG_BASE:SEG_BASE + CODE_LEN])
    # input block
    uc.mem_write(IN_LIN, block[:IN_LEN])

    # stack frame for a far call to 0x61f4
    sp = 0x0F00
    frame = struct.pack("<HHHHH",
                        0x0000,   # bp+2  ret_off
                        0xF000,   # bp+4  ret_seg  -> linear 0xF0000
                        IN_SEG,   # bp+6  arg0 input segment
                        0x0000,   # bp+8  arg1 input offset
                        OUT_SEG)  # bp+0xa arg2 output segment
    uc.mem_write(STACK_LIN + sp, frame)

    uc.reg_write(UC_X86_REG_CS, CODE_SEG)
    uc.reg_write(UC_X86_REG_SS, STACK_SEG)
    uc.reg_write(UC_X86_REG_SP, sp)
    uc.reg_write(UC_X86_REG_DS, 0)
    uc.reg_write(UC_X86_REG_ES, 0)
    uc.reg_write(UC_X86_REG_IP, DECODER_IP)

    writes = {"lo": OUT_LEN, "hi": 0}

    def on_write(uc_, access, addr, size, value, user):
        if OUT_LIN <= addr < OUT_LIN + OUT_LEN:
            off = addr - OUT_LIN
            writes["lo"] = min(writes["lo"], off)
            writes["hi"] = max(writes["hi"], off + size)

    def on_unmapped(uc_, access, addr, size, value, user):
        print(f"  !! unmapped access @ 0x{addr:x} size {size}")
        return False

    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_unmapped)

    try:
        uc.emu_start(CODE_LIN + DECODER_IP, RET_LIN, count=20_000_000)
    except UcError as e:
        ip = uc.reg_read(UC_X86_REG_IP)
        print(f"  UcError: {e}  at cs-off 0x{ip:x} (file 0x{ip + SEG_BASE:x})")

    ax = uc.reg_read(UC_X86_REG_AX)
    di = uc.reg_read(UC_X86_REG_DI)
    out = uc.mem_read(OUT_LIN, max(writes["hi"], 1))
    # 输入流偏移在栈帧 [bp+8] = STACK_LIN + 0xF06 (bp = 0xEFE)
    consumed = struct.unpack("<H", uc.mem_read(STACK_LIN + 0xF06, 2))[0]
    if trace:
        print(f"  ret AX=0x{ax:04x}  DI=0x{di:x}  写出 [0x{writes['lo']:x},0x{writes['hi']:x})  "
              f"消耗输入 {consumed}  w={width} h={height}")
    return bytes(out), di, width, height, consumed


def deplanar(out: bytes, w: int, h: int):
    """4bpp planar, byte-interleaved: 每 8 像素列有连续 4 字节 (4 plane)。
    返回 PIL 'P' 索引图 (0..15)。"""
    from PIL import Image
    im = Image.new("P", (w, h))
    px = im.load()
    sp = w // 8
    need = sp * h * 4
    if len(out) < need:
        out = out + b"\x00" * (need - len(out))
    for y in range(h):
        for xb in range(sp):
            base = (y * sp + xb) * 4
            b0, b1, b2, b3 = out[base], out[base + 1], out[base + 2], out[base + 3]
            for k in range(8):
                bit = 7 - k
                c = (((b0 >> bit) & 1) | (((b1 >> bit) & 1) << 1)
                     | (((b2 >> bit) & 1) << 2) | (((b3 >> bit) & 1) << 3))
                px[xb * 8 + k, y] = c
    return im


# placeholder 16-color palette (PC-98-ish) until the real one is found
_PAL = []
for i in range(16):
    r = (i & 1) * 0xAA + (i & 8) // 8 * 0x55
    g = ((i >> 1) & 1) * 0xAA + (i & 8) // 8 * 0x55
    b = ((i >> 2) & 1) * 0xAA + (i & 8) // 8 * 0x55
    _PAL += [r, g, b]


def parse_blocks(fn: str):
    data = Path(fn).read_bytes()
    n = struct.unpack(">I", data[0:4])[0] // 4
    offs = [struct.unpack(">I", data[i * 4:i * 4 + 4])[0] for i in range(n)]
    offs.append(len(data))
    return [data[offs[i]:offs[i + 1]] for i in range(n)]


if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "/Users/dong/Projects/Koukai2/Endgrp.dat"
    blocks = parse_blocks(fn)
    name = Path(fn).stem.lower()
    outdir = Path(__file__).resolve().parent.parent / "output" / f"eventcg_{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for i, block in enumerate(blocks):
        w, h = struct.unpack_from("<HH", block, 0)
        out, di, _, _, consumed = decode_block(block)
        need = (w // 8) * h * 4
        tail = len(block) - consumed
        if len(out) < need or di != 0:
            print(f"  block {i}: w={w} h={h} 输出不足/DI 异常 (>64K?) — 跳过")
            continue
        if tail not in (0, 1):
            print(f"  block {i}: w={w} h={h} 尾部剩余 {tail} 字节")
        im = deplanar(out, w, h)
        im.putpalette(_PAL)
        im.convert("RGB").save(outdir / f"{i:03d}.png")
        ok += 1
    print(f"{name}: {ok}/{len(blocks)} 解码成功 -> {outdir}")
