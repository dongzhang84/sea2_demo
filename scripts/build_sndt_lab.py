#!/usr/bin/env python3
"""Build minimal SNDT lab artifacts without modifying game_dos/.

The lab creates a controlled SNRDAT archive where one selected subscript's
bytecode area is replaced with a minimal known program:

  0c <text_id> f2

Known facts:
- 0x0c displays one Snr*.mes text entry.
- 0xf2 terminates a subscript.

The original SNDT container, chunk table, subscript table, and dispatch table
are preserved. Only the bytecode area after the dispatch table is patched.
Outputs live under output/sndt_lab/ and are safe to inspect before manually
copying into any runnable game directory.
"""
from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_lab"


@dataclass
class Target:
    snr_id: int
    chunk_id: int
    sub_id: int
    text_id: int


DEFAULT_TARGET = Target(snr_id=4, chunk_id=0, sub_id=0, text_id=0)


def read_u16be(data: bytes, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def read_u32be(data: bytes, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]


def parse_chunks(data: bytes) -> list[tuple[int, int, list[int]]]:
    if data[:4] != b"SNDT":
        raise ValueError("not an SNDT file")
    offsets: list[int] = []
    pos = 0x10
    while pos + 4 <= len(data):
        value = read_u32be(data, pos)
        pos += 4
        if value == 0xFFFFFFFF:
            break
        offsets.append(value)
    bounds = offsets + [len(data)]
    chunks: list[tuple[int, int, list[int]]] = []
    for start, end in zip(bounds, bounds[1:]):
        subs: list[int] = []
        pos = start
        while pos + 2 <= end:
            value = read_u16be(data, pos)
            pos += 2
            if value == 0xFFFF:
                break
            subs.append(value)
        chunks.append((start, end, subs))
    return chunks


def parse_dispatch_end(data: bytes, start: int, end: int) -> int:
    pos = start
    while pos + 2 <= end:
        key = read_u16be(data, pos)
        if key == 0xFFFF:
            pos += 2
            if pos + 2 <= end and read_u16be(data, pos) == 0xFFFF:
                pos += 2
            return pos
        pos += 4
    raise ValueError(f"dispatch table did not terminate between 0x{start:x} and 0x{end:x}")


def patch_target(parts: list[bytes], target: Target) -> tuple[list[bytes], dict]:
    patched = list(parts)
    data = bytearray(patched[target.snr_id])
    chunks = parse_chunks(data)
    chunk_start, chunk_end, subs = chunks[target.chunk_id]
    sub_starts = [chunk_start + rel for rel in subs] + [chunk_end]
    sub_start = sub_starts[target.sub_id]
    sub_end = sub_starts[target.sub_id + 1]
    code_start = parse_dispatch_end(data, sub_start, sub_end)
    code_len = sub_end - code_start
    if code_len < 3:
        raise ValueError(f"target code area too small: {code_len} bytes")

    original_head = bytes(data[code_start : min(sub_end, code_start + 32)])
    program = bytes([0x0C, target.text_id, 0xF2])
    filler = bytes([0xF2]) * (code_len - len(program))
    data[code_start:sub_end] = program + filler
    patched[target.snr_id] = bytes(data)

    return patched, {
        "target": {
            "snr": target.snr_id,
            "chunk": target.chunk_id,
            "subscript": target.sub_id,
            "text_id": target.text_id,
        },
        "sub_start": sub_start,
        "sub_end": sub_end,
        "code_start": code_start,
        "code_len": code_len,
        "program_hex": program.hex(" "),
        "original_head_hex": original_head.hex(" "),
        "patched_head_hex": bytes(data[code_start : min(sub_end, code_start + 32)]).hex(" "),
    }


def encode_part(raw: bytes) -> bytes:
    bits: list[int] = []
    for byte in raw:
        width = 1
        while not (2**width - 2 <= byte <= 2 ** (width + 1) - 3):
            width += 1
        factor = byte - (2**width - 2)
        bits.extend([1] * (width - 1))
        bits.append(0)
        for i in range(width - 1, -1, -1):
            bits.append((factor >> i) & 1)

    out = bytearray()
    for i in range(0, len(bits), 8):
        chunk = bits[i : i + 8]
        chunk += [0] * (8 - len(chunk))
        value = 0
        for bit in chunk:
            value = (value << 1) | bit
        out.append(value)
    return bytes(out)


def build_ls11_archive(parts: list[bytes]) -> bytes:
    encoded = [encode_part(part) for part in parts]
    index_len = 12 * len(parts) + 4
    data_start = 16 + 256 + index_len
    out = bytearray()
    out += b"LS11"
    out += b"\x00" * 12
    out += bytes(range(256))
    offset = data_start
    for raw, enc in zip(parts, encoded):
        out += len(enc).to_bytes(4, "big")
        out += len(raw).to_bytes(4, "big")
        out += offset.to_bytes(4, "big")
        offset += len(enc)
    out += b"\x00\x00\x00\x00"
    for enc in encoded:
        out += enc
    return bytes(out)


def write_patch_notes(info: dict, archive_path: Path, patched_dat_path: Path) -> None:
    lines = [
        "# SNDT Lab Patch Notes",
        "",
        "This lab artifact preserves the SNDT container and dispatch table,",
        "but replaces one subscript bytecode area with a minimal known program.",
        "",
        "## Target",
        "",
        f"- SNDT file: `Snr{info['target']['snr']}.dat`",
        f"- Chunk: `{info['target']['chunk']}`",
        f"- Subscript: `{info['target']['subscript']}`",
        f"- Text id: `{info['target']['text_id']}`",
        f"- Subscript range: `0x{info['sub_start']:04x}..0x{info['sub_end']:04x}`",
        f"- Code start: `0x{info['code_start']:04x}`",
        f"- Code length: `{info['code_len']}` bytes",
        "",
        "## Program",
        "",
        "```text",
        "0c <text_id> f2",
        "```",
        "",
        f"- Program bytes: `{info['program_hex']}`",
        f"- Original head: `{info['original_head_hex']}`",
        f"- Patched head: `{info['patched_head_hex']}`",
        "",
        "## Outputs",
        "",
        f"- Patched DAT: `{patched_dat_path.relative_to(ROOT)}`",
        f"- Rebuilt archive: `{archive_path.relative_to(ROOT)}`",
        "",
        "These files are not copied into `game_dos/` automatically.",
    ]
    (OUT_DIR / "patch_notes.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parts = [(KOUKAI / f"Snr{i}.dat").read_bytes() for i in range(7)]
    patched, info = patch_target(parts, DEFAULT_TARGET)

    patched_dat = OUT_DIR / "Snr4_min_text_c0s0.dat"
    archive = OUT_DIR / "SNRDAT_min_snr4_c0s0.LZW"
    info_json = OUT_DIR / "patch_info.json"

    patched_dat.write_bytes(patched[DEFAULT_TARGET.snr_id])
    archive.write_bytes(build_ls11_archive(patched))
    info_json.write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n")
    write_patch_notes(info, archive, patched_dat)

    print(f"Wrote {patched_dat}")
    print(f"Wrote {archive}")
    print(f"Wrote {info_json}")
    print(f"Wrote {OUT_DIR / 'patch_notes.md'}")


if __name__ == "__main__":
    main()
