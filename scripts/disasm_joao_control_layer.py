#!/usr/bin/env python3
"""Prototype disassembly of João residual control layer with candidate lengths."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_analysis"
CONTROL = OUT_DIR / "joao_control_candidates.json"
SCRIPT_ID = "Snr1.chunk0.sub0"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402
from sndt_disasm import parse_code_areas  # noqa: E402


OPCODES = {
    0xAD: ("ad_control", 4),
    0xAC: ("ac_control", 4),
    0xFE: ("fe_control", 3),
    0xF8: ("f8_prefix_or_branch", 1),
    0xF9: ("f9_control", 3),
    0xFB: ("fb_control", 2),
    0x8C: ("8c_control", 5),
    0x8F: ("8f_control", 4),
    0xDC: ("dc_control", 4),
    0x2C: ("2c_control", 3),
    0x0F: ("0f_control", 3),
    0x1D: ("1d_control", 3),
    0x4C: ("4c_control", 3),
    0x15: ("15_control", 5),
    0x11: ("11_control", 3),
    0x2E: ("2e_control", 2),
    0x8D: ("8d_control", 3),
    0xE6: ("e6_control", 2),
    0xE9: ("e9_control", 2),
    0xEB: ("eb_control", 4),
    0xFA: ("fa_control", 4),
    0xC9: ("c9_control", 4),
    0xF0: ("f0_control", 1),
    0xF2: ("end_subscript", 1),
}


def decode_arg(raw: bytes) -> int | None:
    if len(raw) == 1:
        return None
    value = 0
    for byte in raw[1:]:
        value = (value << 8) | byte
    return value


def disasm_span(code: bytes, start: int, end: int, texts: list[str]) -> tuple[list[dict], int]:
    pos = start
    insns = []
    unknown = 0
    while pos < end:
        op = code[pos]
        text = None
        if op == 0x0C and pos + 1 < end:
            name = "show_text_byte"
            length = 2
            text_id = code[pos + 1]
            text = texts[text_id] if text_id < len(texts) else ""
        else:
            name, length = OPCODES.get(op, (f"db_{op:02x}", 1))
        if pos + length > end:
            name = f"db_{op:02x}"
            length = 1
        raw = code[pos : pos + length]
        if name.startswith("db_"):
            unknown += 1
        insns.append(
            {
                "offset": pos,
                "offset_hex": f"0x{pos:04x}",
                "op": name,
                "bytes": raw.hex(" "),
                "arg": decode_arg(raw),
                "text": text,
            }
        )
        pos += length
    return insns, unknown


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    control = json.loads(CONTROL.read_text())
    area = next(area for area in parse_code_areas(1) if area["id"] == SCRIPT_ID)
    code = area["code"]
    texts = decode_file(str(KOUKAI / "Snr1.mes"))

    spans = []
    totals = {"instructions": 0, "unknown_bytes": 0, "residual_bytes": 0}
    opcode_counts = {}
    for span in control["residual_spans"]:
        insns, unknown = disasm_span(code, span["start"], span["end"], texts)
        totals["instructions"] += len(insns)
        totals["unknown_bytes"] += unknown
        totals["residual_bytes"] += span["length"]
        for insn in insns:
            opcode_counts[insn["op"]] = opcode_counts.get(insn["op"], 0) + 1
        spans.append(
            {
                "start": span["start"],
                "start_hex": span["start_hex"],
                "end": span["end"],
                "end_hex": span["end_hex"],
                "length": span["length"],
                "unknown_bytes": unknown,
                "instructions": insns,
            }
        )

    result = {
        "schema": "joao_control_layer_disasm_v0",
        "source_script": SCRIPT_ID,
        "warning": "Prototype candidate-length disassembly; opcode semantics are not confirmed.",
        "candidate_lengths": {f"{op:02x}": {"name": name, "length": length} for op, (name, length) in OPCODES.items()},
        "summary": totals,
        "opcode_counts": dict(sorted(opcode_counts.items(), key=lambda item: (-item[1], item[0]))),
        "spans": spans,
    }
    (OUT_DIR / "joao_control_disasm.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# João Control Layer Prototype Disassembly",
        "",
        "Prototype disassembly over residual bytes after long and short text motifs are removed.",
        "This tests candidate lengths only; names and semantics are not confirmed.",
        "",
        f"- Residual bytes: `{totals['residual_bytes']}`",
        f"- Instructions: `{totals['instructions']}`",
        f"- Unknown bytes: `{totals['unknown_bytes']}`",
        "",
        "## Opcode Counts",
        "",
    ]
    for op, count in result["opcode_counts"].items():
        lines.append(f"- `{op}`: {count}")
    lines += ["", "## Spans", ""]
    for span in spans:
        lines += [
            f"### {span['start_hex']}..{span['end_hex']}",
            "",
            f"- Length: `{span['length']}`",
            f"- Unknown bytes: `{span['unknown_bytes']}`",
            "",
            "```text",
        ]
        for insn in span["instructions"]:
            arg = "" if insn["arg"] is None else f" {insn['arg']}"
            text = ""
            if insn.get("text"):
                text = " ; " + insn["text"].replace("\n", "\\n")[:80]
            lines.append(f"{insn['offset_hex']}: {insn['bytes']:<14} {insn['op']}{arg}{text}")
        lines += ["```", ""]

    lines += ["## Interpretation", ""]
    lines += [
        "- This candidate length table covers most residual control bytes but still leaves unknown singletons.",
        "- Clean 4-byte `ad/ac` and 5-byte `8c` records often point at nearby bytecode offsets, so they are strong branch/call candidates.",
        "- `fe` consistently decodes as a 3-byte form in this slice.",
        "- Remaining unknown bytes should be checked against neighboring spans before being added to the global opcode table.",
    ]
    (OUT_DIR / "joao_control_disasm.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'joao_control_disasm.json'}")
    print(f"Wrote {OUT_DIR / 'joao_control_disasm.md'}")


if __name__ == "__main__":
    main()
