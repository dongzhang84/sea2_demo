#!/usr/bin/env python3
"""Disassemble ranges of Koukai2/Main.exe (PC-98 16-bit MZ).

事件 CG 解码攻坚用的反汇编工具。

用法:
  disasm_exe.py <vaddr_hex> <count>     反汇编从 CS 相对地址 vaddr 起的 count 条指令
  disasm_exe.py find <hexbytes>         搜索字节序列, 打印 file offset 与 vaddr
  disasm_exe.py bytes <vaddr_hex> <n>   hexdump n 字节

地址约定: 反汇编/参数里的地址都是【文件偏移】(跟 main_exe_decoder_disasm.txt 一致)。
CS 相对地址 → 文件偏移 = cs_addr + 0x5200 (MZ 头 0x5200, cs=0)。
所以代码里的 cs:[0xbbc] 等表, 文件偏移 = 0xbbc + 0x5200。
"""
import sys
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_16

EXE = Path("/Users/dong/Projects/Koukai2/Main.exe")
SEG_BASE = 0x5200   # file offset of cs:0 — add to CS-relative addrs

_data = EXE.read_bytes()
_md = Cs(CS_ARCH_X86, CS_MODE_16)


def v2f(vaddr: int) -> int:
    return vaddr   # args are file offsets directly


def disasm(vaddr: int, count: int) -> None:
    foff = v2f(vaddr)
    code = _data[foff:foff + count * 8 + 16]
    n = 0
    for insn in _md.disasm(code, vaddr):
        hexb = insn.bytes.hex()
        print(f"  0x{insn.address:06x}: {hexb:<16} {insn.mnemonic:<7} {insn.op_str}")
        n += 1
        if n >= count:
            break


def find(hexbytes: str) -> None:
    pat = bytes.fromhex(hexbytes)
    start = 0
    hits = 0
    while True:
        i = _data.find(pat, start)
        if i < 0:
            break
        print(f"  file 0x{i:06x}   vaddr 0x{i - CODE_BASE:06x}")
        start = i + 1
        hits += 1
        if hits > 40:
            print("  ... (more)")
            break
    if hits == 0:
        print("  not found")


def dump_bytes(vaddr: int, n: int) -> None:
    foff = v2f(vaddr)
    chunk = _data[foff:foff + n]
    for row in range(0, len(chunk), 16):
        seg = chunk[row:row + 16]
        hexs = " ".join(f"{b:02x}" for b in seg)
        print(f"  0x{vaddr + row:06x}: {hexs}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "find":
        find(args[1])
    elif args[0] == "bytes":
        dump_bytes(int(args[1], 16), int(args[2]))
    else:
        disasm(int(args[0], 16), int(args[1]))
