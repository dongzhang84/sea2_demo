#!/usr/bin/env python3
"""Scan Main.exe for LS11-like decoder signatures.

LS11 decoder reads bits one-by-one, finds the first 0 bit to get mask_len,
reads mask_len more bits for factor, computes code = (1<<mask_len) - 2 + factor,
then either looks up dictionary[code] (0..255) or does back-reference.

x86-16 signatures to look for:
  - Repeated SHL byte, 1 / TEST AL, AL pattern for bit reading
  - (1 << n) - 2 sequence (SHL/SUB by 2)
  - Byte table indexing with offset ~256
  - Calls referencing data at offset 0x38be2 (GRAPH.DAT string)
"""
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16

EXE_PATH = Path('/Users/dong/Projects/Koukai2/Main.exe')
HDR_SIZE = 0x5200
CODE = EXE_PATH.read_bytes()[HDR_SIZE:]

md = Cs(CS_ARCH_X86, CS_MODE_16)
md.detail = True

# Search for LS11 byte signatures based on our Python decoder.
# The most distinctive part is the "(1 << mask_len) - 2 + factor" computation.
# In x86: MOV CX,n / MOV AX,1 / SHL AX,CL / SUB AX,2 / ADD AX,factor
# That's the bytes: 8b c8 or B9 xx xx / B8 01 00 / D3 E0 / 83 E8 02

# Simpler: look for the 256-byte dictionary copy.
# LS11 reads 256 bytes from offset 16 into a buffer. The decoder uses that
# buffer for code < 256 lookups. So somewhere we should see a 256-byte
# memcpy with literal length 256 / 100h.

# Let's hunt for "MOV CX, 100h" (B9 00 01) followed soon by REP MOVS (F3 A4 or F3 A5)
print("=== Searching for REP MOVSB/W with CX=256 pattern ===")
needle = bytes([0xB9, 0x00, 0x01])  # MOV CX, 0x100
positions = []
i = 0
while i < len(CODE) - 3:
    p = CODE.find(needle, i)
    if p < 0: break
    # Check next ~20 bytes for REP MOVS
    follow = CODE[p+3:p+24]
    if b'\xF3\xA4' in follow or b'\xF3\xA5' in follow:
        positions.append(p)
    i = p + 1
print(f"  found {len(positions)} candidate locations (with MOV CX,0x100 + REP MOVS soon after)")
for p in positions[:10]:
    abs_addr = p + HDR_SIZE
    print(f"  file offset 0x{abs_addr:06x}  context: {CODE[p:p+16].hex()}")

# Now disassemble around each candidate
print(f"\n=== Disassembly around first 3 candidates ===")
for p in positions[:3]:
    abs_addr = p + HDR_SIZE
    print(f"\n--- 0x{abs_addr:06x} ---")
    chunk = CODE[max(0, p-32):p+64]
    for ins in md.disasm(chunk, abs_addr - 32):
        print(f"  0x{ins.address:06x}: {ins.mnemonic:<8} {ins.op_str}")
        if ins.address > abs_addr + 32:
            break

# Also look for the bit-loop signature: "shl ..., 1" repeated tightly with counter
# In bytes: D0 ?? (SHL r/m8, 1) — D0 followed by mod-r/m byte
# Often: D0 06 [addr16] (SHL byte [addr], 1) or D0 E0..E7 (SHL reg, 1)
print(f"\n=== Tight bit-shift loops (3+ SHL byte,1 in 12 bytes) ===")
shift_op = bytes([0xD0])
# Scan for clusters
counts = {}
for i in range(len(CODE) - 12):
    window = CODE[i:i+12]
    n = sum(1 for j in range(0, 11) if window[j] == 0xD0 and window[j+1] in range(0xE0, 0xF8))
    if n >= 3:
        counts[i] = n
top = sorted(counts.items(), key=lambda x: -x[1])[:10]
for p, n in top:
    abs_addr = p + HDR_SIZE
    print(f"  0x{abs_addr:06x}: {n} SHLs / window  ({CODE[p:p+12].hex()})")
