#!/usr/bin/env python3
"""Analyze non-motif bytecode gaps in João's opening topology slice."""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_analysis"
TOPOLOGY = ROOT / "output" / "sndt_topology" / "joao_opening_topology.json"
SCRIPT_ID = "Snr1.chunk0.sub0"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402
from sndt_disasm import parse_code_areas  # noqa: E402


def u16be(data: bytes, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def decode_known(code: bytes, base: int, texts: list[str]) -> list[dict]:
    items = []
    pos = 0
    while pos < len(code):
        op = code[pos]
        offset = base + pos
        if op == 0x0C and pos + 1 < len(code):
            text_id = code[pos + 1]
            items.append(
                {
                    "offset": offset,
                    "offset_hex": f"0x{offset:04x}",
                    "bytes": code[pos : pos + 2].hex(" "),
                    "op": "show_text",
                    "args": [text_id],
                    "text": texts[text_id] if text_id < len(texts) else "",
                }
            )
            pos += 2
        elif op == 0xF2:
            items.append({"offset": offset, "offset_hex": f"0x{offset:04x}", "bytes": "f2", "op": "end_subscript", "args": []})
            pos += 1
        elif op == 0xC0 and pos + 1 < len(code):
            items.append({"offset": offset, "offset_hex": f"0x{offset:04x}", "bytes": code[pos : pos + 2].hex(" "), "op": "c0", "args": [code[pos + 1]]})
            pos += 2
        elif op in (0xCC, 0xC8) and pos + 2 < len(code):
            arg = u16be(code, pos + 1)
            items.append({"offset": offset, "offset_hex": f"0x{offset:04x}", "bytes": code[pos : pos + 3].hex(" "), "op": f"{op:02x}", "args": [arg]})
            pos += 3
        elif op == 0xC7:
            items.append({"offset": offset, "offset_hex": f"0x{offset:04x}", "bytes": "c7", "op": "c7", "args": []})
            pos += 1
        else:
            items.append({"offset": offset, "offset_hex": f"0x{offset:04x}", "bytes": f"{op:02x}", "op": "db", "args": [op]})
            pos += 1
    return items


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    topology = json.loads(TOPOLOGY.read_text())
    scenes = topology["scenes"]
    texts = decode_file(str(KOUKAI / "Snr1.mes"))
    area = next(area for area in parse_code_areas(1) if area["id"] == SCRIPT_ID)
    code = area["code"]

    seen_texts = {record["text_id"] for scene in scenes for record in scene["records"]}
    missing_texts = [
        {"text_id": text_id, "text": texts[text_id]}
        for text_id in range(min(seen_texts), max(seen_texts) + 1)
        if text_id not in seen_texts and text_id < len(texts)
    ]

    boundaries = []
    previous_end = 0
    for index, scene in enumerate(scenes):
        if scene["start"] > previous_end:
            boundaries.append((f"gap_before_scene_{index:02d}", previous_end, scene["start"]))
        previous_end = scene["end"]
    if previous_end < len(code):
        boundaries.append(("gap_after_last_scene", previous_end, len(code)))

    gaps = []
    for name, start, end in boundaries:
        gap_code = code[start:end]
        instructions = decode_known(gap_code, start, texts)
        embedded_texts = []
        for pos, byte in enumerate(gap_code[:-1]):
            if byte != 0x0C:
                continue
            text_id = gap_code[pos + 1]
            if text_id < len(texts):
                embedded_texts.append({"offset_hex": f"0x{start + pos:04x}", "text_id": text_id, "text": texts[text_id]})
        gaps.append(
            {
                "id": name,
                "start": start,
                "start_hex": f"0x{start:04x}",
                "end": end,
                "end_hex": f"0x{end:04x}",
                "length": end - start,
                "bytes": gap_code.hex(" "),
                "known_ops": [item for item in instructions if item["op"] != "db"],
                "unknown_byte_count": sum(1 for item in instructions if item["op"] == "db"),
                "embedded_text_refs": embedded_texts,
                "instructions": instructions,
            }
        )

    result = {
        "schema": "joao_opening_gap_analysis_v1",
        "source_script": SCRIPT_ID,
        "code_len": len(code),
        "summary": {
            "scene_count": len(scenes),
            "gap_count": len(gaps),
            "gap_bytes": sum(gap["length"] for gap in gaps),
            "missing_text_count": len(missing_texts),
        },
        "missing_texts": missing_texts,
        "gaps": gaps,
    }
    (OUT_DIR / "joao_opening_gaps.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# João Opening Non-Motif Gaps",
        "",
        "This reports bytecode gaps between `c0/cc/c8/c7` motif runs in `Snr1.chunk0.sub0`.",
        "These gaps are candidates for branch, condition, state mutation, and non-motif text handling.",
        "",
        f"- Scenes: `{len(scenes)}`",
        f"- Gaps: `{len(gaps)}`",
        f"- Gap bytes: `{sum(gap['length'] for gap in gaps)}`",
        f"- Missing text ids inside motif range: `{len(missing_texts)}`",
        "",
        "## Missing Text IDs",
        "",
    ]
    for item in missing_texts:
        text = item["text"].replace("\n", "\\n")
        lines.append(f"- `{item['text_id']}`: {text}")

    lines += ["", "## Gaps", ""]
    for gap in gaps:
        lines += [
            f"### {gap['id']}",
            "",
            f"- Offset: `{gap['start_hex']}..{gap['end_hex']}`",
            f"- Length: `{gap['length']}`",
            f"- Unknown bytes: `{gap['unknown_byte_count']}`",
            f"- Embedded text refs: `{len(gap['embedded_text_refs'])}`",
            "",
            "```text",
        ]
        for item in gap["instructions"][:120]:
            args = " ".join(str(arg) for arg in item["args"])
            suffix = ""
            if item["op"] == "show_text":
                suffix = " ; " + item["text"].replace("\n", "\\n")[:80]
            lines.append(f"{item['offset_hex']}: {item['bytes']:<10} {item['op']} {args}{suffix}".rstrip())
        if len(gap["instructions"]) > 120:
            lines.append("...")
        lines += ["```", ""]
    (OUT_DIR / "joao_opening_gaps.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'joao_opening_gaps.json'}")
    print(f"Wrote {OUT_DIR / 'joao_opening_gaps.md'}")


if __name__ == "__main__":
    main()
