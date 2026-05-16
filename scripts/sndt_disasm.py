#!/usr/bin/env python3
"""Partial SNDT disassembler using confirmed/candidate opcode lengths."""
from __future__ import annotations

import json
import struct
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_analysis"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402


def u16be(data: bytes, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def u32be(data: bytes, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]


def parse_code_areas(snr_id: int) -> list[dict]:
    path = KOUKAI / f"Snr{snr_id}.dat"
    data = path.read_bytes()
    offsets: list[int] = []
    pos = 0x10
    while True:
        value = u32be(data, pos)
        pos += 4
        if value == 0xFFFFFFFF:
            break
        offsets.append(value)
    bounds = offsets + [len(data)]

    areas: list[dict] = []
    for ci, (start, end) in enumerate(zip(bounds, bounds[1:])):
        subs: list[int] = []
        pos = start
        while pos + 2 <= end:
            value = u16be(data, pos)
            pos += 2
            if value == 0xFFFF:
                break
            subs.append(value)
        sub_abs = [start + rel for rel in subs] + [end]
        for si in range(len(subs)):
            sub_start = sub_abs[si]
            sub_end = sub_abs[si + 1]
            pos = sub_start
            dispatch = []
            while pos + 2 <= sub_end:
                key = u16be(data, pos)
                if key == 0xFFFF:
                    pos += 2
                    if pos + 2 <= sub_end and u16be(data, pos) == 0xFFFF:
                        pos += 2
                    break
                target = u16be(data, pos + 2)
                dispatch.append({"key": key, "target": target})
                pos += 4
            areas.append(
                {
                    "id": f"Snr{snr_id}.chunk{ci}.sub{si}",
                    "snr": snr_id,
                    "chunk": ci,
                    "sub": si,
                    "sub_start": sub_start,
                    "sub_end": sub_end,
                    "code_start": pos,
                    "dispatch": dispatch,
                    "code": data[pos:sub_end],
                }
            )
    return areas


def disasm_code(code: bytes, texts: list[str]) -> tuple[list[dict], dict]:
    pos = 0
    insns = []
    stats = {"known": 0, "unknown": 0, "text_refs": 0}
    while pos < len(code):
        op = code[pos]
        start = pos
        if op == 0x0C and pos + 1 < len(code):
            text_id = code[pos + 1]
            text = texts[text_id] if text_id < len(texts) else ""
            insns.append(
                {
                    "offset": start,
                    "bytes": code[start : start + 2].hex(" "),
                    "op": "show_text",
                    "args": [text_id],
                    "text": text,
                }
            )
            stats["known"] += 1
            stats["text_refs"] += 1
            pos += 2
        elif op == 0xF2:
            insns.append({"offset": start, "bytes": "f2", "op": "end_subscript", "args": []})
            stats["known"] += 1
            pos += 1
        elif op == 0xC0 and pos + 1 < len(code):
            insns.append({"offset": start, "bytes": code[start : start + 2].hex(" "), "op": "c0", "args": [code[pos + 1]]})
            stats["known"] += 1
            pos += 2
        elif op in (0xCC, 0xC8) and pos + 2 < len(code):
            arg = (code[pos + 1] << 8) | code[pos + 2]
            insns.append({"offset": start, "bytes": code[start : start + 3].hex(" "), "op": f"{op:02x}", "args": [arg]})
            stats["known"] += 1
            pos += 3
        elif op == 0xC7:
            insns.append({"offset": start, "bytes": "c7", "op": "c7", "args": []})
            stats["known"] += 1
            pos += 1
        else:
            insns.append({"offset": start, "bytes": f"{op:02x}", "op": "db", "args": [op]})
            stats["unknown"] += 1
            pos += 1
    return insns, stats


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    totals = {"known": 0, "unknown": 0, "text_refs": 0, "areas": 0}
    for snr_id in range(7):
        texts = decode_file(str(KOUKAI / f"Snr{snr_id}.mes"))
        areas_out = []
        for area in parse_code_areas(snr_id):
            insns, stats = disasm_code(area["code"], texts)
            totals["areas"] += 1
            for key in ("known", "unknown", "text_refs"):
                totals[key] += stats[key]
            areas_out.append(
                {
                    "id": area["id"],
                    "code_start": area["code_start"],
                    "code_len": len(area["code"]),
                    "dispatch": area["dispatch"],
                    "stats": stats,
                    "instructions": insns,
                }
            )
        files.append({"id": f"Snr{snr_id}", "areas": areas_out})

    out = {"schema": "sndt_partial_disasm_v1", "totals": totals, "files": files}
    (OUT_DIR / "sndt_disasm_partial.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# SNDT Partial Disassembly",
        "",
        "Recognized opcodes: `0x0c`, `0xf2`, `0xc0`, `0xcc`, `0xc8`, `0xc7`.",
        "Unknown bytes are emitted as `db`.",
        "",
        f"- Areas: `{totals['areas']}`",
        f"- Known instructions: `{totals['known']}`",
        f"- Unknown bytes: `{totals['unknown']}`",
        f"- Boundary-aligned text refs: `{totals['text_refs']}`",
        "",
    ]
    for file_info in files:
        lines.append(f"## {file_info['id']}")
        lines.append("")
        for area in file_info["areas"][:8]:
            lines.append(f"### {area['id']}")
            lines.append("")
            lines.append(
                f"- code_start: `0x{area['code_start']:04x}`, code_len: `{area['code_len']}`, "
                f"known: `{area['stats']['known']}`, unknown: `{area['stats']['unknown']}`, "
                f"text_refs: `{area['stats']['text_refs']}`"
            )
            lines.append("")
            lines.append("```text")
            for ins in area["instructions"][:80]:
                args = " ".join(str(a) for a in ins["args"])
                text = ""
                if ins["op"] == "show_text":
                    text = " ; " + ins["text"].replace("\n", "\\n")[:80]
                lines.append(f"{ins['offset']:04x}: {ins['bytes']:<10} {ins['op']} {args}{text}".rstrip())
            if len(area["instructions"]) > 80:
                lines.append("...")
            lines.append("```")
            lines.append("")
    (OUT_DIR / "sndt_disasm_partial.md").write_text("\n".join(lines))
    print(f"Wrote {OUT_DIR / 'sndt_disasm_partial.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_disasm_partial.md'}")


if __name__ == "__main__":
    main()
