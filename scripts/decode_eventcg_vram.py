#!/usr/bin/env python3
"""事件 CG 大图解码器 —— 模拟 Main.exe 的 VRAM 解码器 (0x5dcc/0x5e00)。

缓冲区解码器 (0x61f4) 的 16 位 DI 装不下 640×400。VRAM 解码器把图写进
VGA 的 4 个 plane (每 plane 独立寻址, DI 不溢出)。这里用 unicorn 跑原始
代码, 并实现一个 VGA write-mode-0 模型 (latch / map-mask / bit-mask)。

入口 0x61b8 (far): args [bp+6]=x, [bp+8]=y, [bp+0xa]=字节读取器 far 指针。
字节读取器用 `lcall [bp+0xa]` (机器码 ff 5e 0a) —— 我们拦截它直接喂字节。
"""
import struct
import sys
from pathlib import Path

from unicorn import (Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_INSN,
                     UC_HOOK_MEM_UNMAPPED, UcError)
from unicorn.x86_const import (UC_X86_REG_CS, UC_X86_REG_SS, UC_X86_REG_SP,
                               UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_IP,
                               UC_X86_REG_AX, UC_X86_INS_OUT)

EXE = Path("/Users/dong/Projects/Koukai2/Main.exe")
SEG_BASE = 0x5200
ENTRY_FOFF = 0x61b8
ENTRY_IP = ENTRY_FOFF - SEG_BASE          # 0xfb8

CODE_LIN = 0x10000; CODE_SEG = 0x1000; CODE_LEN = 0x2000
DS_LIN = 0x20000;   DS_SEG = 0x2000;   DS_LEN = 0x10000
STACK_LIN = 0x30000; STACK_SEG = 0x3000
VGA_LIN = 0xA0000;  VGA_SEG = 0xA000;  VGA_LEN = 0x10000
RET_LIN = 0xF0000

_exe = EXE.read_bytes()


def _ror8(v, n):
    n &= 7
    return ((v >> n) | (v << (8 - n))) & 0xFF


def decode_vram(block: bytes, trace=False, entry_foff=ENTRY_FOFF):
    width, height = struct.unpack_from("<HH", block, 0)
    entry_ip = entry_foff - SEG_BASE

    uc = Uc(UC_ARCH_X86, UC_MODE_16)
    for lin, ln in [(CODE_LIN, CODE_LEN), (DS_LIN, DS_LEN), (STACK_LIN, 0x1000),
                    (VGA_LIN, VGA_LEN), (RET_LIN, 0x1000)]:
        uc.mem_map(lin, ln)
    uc.mem_write(CODE_LIN, _exe[SEG_BASE:SEG_BASE + CODE_LEN])

    # far-call stack frame to 0x61b8
    sp = 0x0F00
    uc.mem_write(STACK_LIN + sp, struct.pack("<HHHHH",
                 0x0000, 0xF000,   # ret off/seg -> 0xF0000
                 0x0000,           # bp+6  x
                 0x0000,           # bp+8  y
                 0x0000))          # bp+0xa reader (intercepted)
    uc.reg_write(UC_X86_REG_CS, CODE_SEG)
    uc.reg_write(UC_X86_REG_SS, STACK_SEG)
    uc.reg_write(UC_X86_REG_SP, sp)
    uc.reg_write(UC_X86_REG_DS, DS_SEG)
    uc.reg_write(UC_X86_REG_ES, 0)
    uc.reg_write(UC_X86_REG_IP, entry_ip)

    # ---- VGA write-mode-0 model ----
    planes = [bytearray(VGA_LEN) for _ in range(4)]
    latch = [0, 0, 0, 0]
    vga = {"seq_idx": 0, "gc_idx": 0, "map_mask": 0xF,
           "read_map": 0, "bitmask": 0xFF, "gc3": 0}
    inp = {"pos": 0}
    dbg = {"writes": 0, "reads": 0, "lcall": 0, "wlo": VGA_LEN, "whi": 0,
           "masks": set(), "bms": set(), "gc3s": set(), "ports": {}}

    def on_out(uc_, port, size, value, user):
        dbg["ports"][port] = dbg["ports"].get(port, 0) + 1
        if port == 0x3C4:                       # seq index (+ data if word)
            vga["seq_idx"] = value & 0xFF
            if size == 2:
                _seq_data(vga["seq_idx"], (value >> 8) & 0xFF)
        elif port == 0x3C5:
            _seq_data(vga["seq_idx"], value & 0xFF)
        elif port == 0x3CE:                     # GC index (+ data if word)
            vga["gc_idx"] = value & 0xFF
            if size == 2:
                _gc_data(vga["gc_idx"], (value >> 8) & 0xFF)
        elif port == 0x3CF:
            _gc_data(vga["gc_idx"], value & 0xFF)

    def _seq_data(idx, data):
        if idx == 2:
            vga["map_mask"] = data & 0xF

    def _gc_data(idx, data):
        if idx == 3:
            vga["gc3"] = data
        elif idx == 4:
            vga["read_map"] = data & 3
        elif idx == 8:
            vga["bitmask"] = data & 0xFF

    def on_read(uc_, access, addr, size, value, user):
        off = addr - VGA_LIN
        if 0 <= off < VGA_LEN:
            dbg["reads"] += 1
            for p in range(4):
                latch[p] = planes[p][off]
            uc.mem_write(addr, bytes([latch[vga["read_map"]]]))

    def on_write(uc_, access, addr, size, value, user):
        off = addr - VGA_LIN
        if not (0 <= off < VGA_LEN):
            return
        dbg["writes"] += 1
        dbg["wlo"] = min(dbg["wlo"], off)
        dbg["whi"] = max(dbg["whi"], off + 1)
        dbg["masks"].add(vga["map_mask"])
        dbg["bms"].add(vga["bitmask"])
        dbg["gc3s"].add(vga["gc3"])
        rot = _ror8(value & 0xFF, vga["gc3"] & 7)
        bm = vga["bitmask"]
        for p in range(4):
            if vga["map_mask"] & (1 << p):
                planes[p][off] = (rot & bm) | (latch[p] & ~bm & 0xFF)

    def on_code(uc_, addr, size, user):
        # 拦截 lcall [bp+0xa]  (ff 5e 0a) —— 当字节读取器
        if uc.mem_read(addr, 3) == b"\xff\x5e\x0a":
            b = block[inp["pos"]] if inp["pos"] < len(block) else 0
            inp["pos"] += 1
            uc.reg_write(UC_X86_REG_AX, b)        # AL=byte, AH=0
            uc.reg_write(UC_X86_REG_IP, (addr & 0xFFFF) - CODE_LIN + 3
                         if False else (addr - CODE_LIN + 3))

    def on_unmapped(uc_, access, addr, size, value, user):
        print(f"  !! unmapped @ 0x{addr:x}")
        return False

    uc.hook_add(UC_HOOK_INSN, on_out, None, 1, 0, UC_X86_INS_OUT)
    uc.hook_add(UC_HOOK_MEM_READ, on_read, None, VGA_LIN, VGA_LIN + VGA_LEN)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write, None, VGA_LIN, VGA_LIN + VGA_LEN)
    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_UNMAPPED, on_unmapped)

    try:
        uc.emu_start(CODE_LIN + entry_ip, RET_LIN, count=40_000_000)
    except UcError as e:
        ip = uc.reg_read(UC_X86_REG_IP)
        print(f"  UcError: {e} at cs-off 0x{ip:x} (file 0x{ip + SEG_BASE:x})")

    if trace:
        print(f"  w={width} h={height}  消耗输入 {inp['pos']}/{len(block)}  "
              f"VGA 写 {dbg['writes']}")
    return planes, width, height, dbg["writes"]


VGA_BASE = 0xC80   # 图在 640x480 里垂直居中, 顶距 40 行
VGA_STRIDE = 80    # VRAM 帧固定 640 宽 = 80 字节/行/plane


def decode_auto(block: bytes):
    """两种模式 (0x61b8 带表 / 0x61cc 无表) 都试, 选 VGA 写入数 == w*h 的。
    返回 (planes, w, h, mode) 或 (None, w, h, None) 若都不对。"""
    w, h = struct.unpack_from("<HH", block, 0)
    target = w * h
    for entry, mode in [(0x61b8, "table"), (0x61cc, "notable")]:
        planes, ww, hh, writes = decode_vram(block, entry_foff=entry)
        if writes == target:
            return planes, ww, hh, mode
    return None, w, h, None


def planes_to_image(planes, w, h, base=VGA_BASE):
    from PIL import Image
    im = Image.new("P", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            byo = base + y * VGA_STRIDE + (x // 8)
            bit = 7 - (x & 7)
            c = 0
            for p in range(4):
                c |= ((planes[p][byo] >> bit) & 1) << p
            px[x, y] = c
    return im


_PAL = []
for i in range(16):
    _PAL += [int(i * 255 / 15)] * 3


def parse_blocks(fn):
    data = Path(fn).read_bytes()
    n = struct.unpack(">I", data[0:4])[0] // 4
    offs = [struct.unpack(">I", data[i * 4:i * 4 + 4])[0] for i in range(n)] + [len(data)]
    return [data[offs[i]:offs[i + 1]] for i in range(n)]


if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "/Users/dong/Projects/Koukai2/Graph.dat"
    blocks = parse_blocks(fn)
    name = Path(fn).stem.lower()
    outdir = Path(__file__).resolve().parent.parent / "output" / f"eventcg_{name}"
    outdir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for i, block in enumerate(blocks):
        w, h = struct.unpack_from("<HH", block, 0)
        planes, ww, hh, mode = decode_auto(block)
        if planes is None:
            print(f"  block {i}: w={w} h={h} 两种模式都不匹配 — 跳过")
            continue
        im = planes_to_image(planes, ww, hh)
        im.putpalette(_PAL)
        im.convert("RGB").save(outdir / f"{i:03d}.png")
        ok += 1
        print(f"  block {i}: {ww}x{hh} [{mode}] -> {i:03d}.png")
    print(f"{name}: {ok}/{len(blocks)} 解码成功 -> {outdir}")
