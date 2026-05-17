#!/usr/bin/env python3
"""Analyze residual control bytes after known João text motifs are removed."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "output" / "sndt_analysis"
TOPOLOGY = ROOT / "output" / "sndt_topology" / "joao_opening_topology.json"
SCRIPT_ID = "Snr1.chunk0.sub0"

sys.path.insert(0, str(ROOT / "scripts"))
from sndt_disasm import parse_code_areas  # noqa: E402


TARGET_OPS = [0xAD, 0xAC, 0xFE, 0xF8, 0xF9, 0xFB, 0xDC, 0x8C, 0x8F, 0x0F, 0x1D, 0x2C]


def hex_bytes(values: bytes | list[int]) -> str:
    return " ".join(f"{value:02x}" for value in values)


def span_kind(item: dict) -> str:
    return item["kind"]


def build_known_spans(topology: dict) -> list[dict]:
    spans = []
    for item in topology["timeline"]:
        spans.append(
            {
                "start": item["start"],
                "end": item["end"],
                "kind": span_kind(item),
                "id": item["id"],
            }
        )
    return sorted(spans, key=lambda span: (span["start"], span["end"]))


def residual_spans(code_len: int, known_spans: list[dict]) -> list[dict]:
    residual = []
    pos = 0
    for span in known_spans:
        if span["start"] > pos:
            residual.append({"start": pos, "end": span["start"]})
        pos = max(pos, span["end"])
    if pos < code_len:
        residual.append({"start": pos, "end": code_len})
    return residual


def neighbor_label(offset: int, known_spans: list[dict]) -> tuple[str | None, str | None]:
    before = None
    after = None
    for span in known_spans:
        if span["end"] <= offset:
            before = span["id"]
        elif span["start"] >= offset and after is None:
            after = span["id"]
            break
    return before, after


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    topology = json.loads(TOPOLOGY.read_text())
    area = next(area for area in parse_code_areas(1) if area["id"] == SCRIPT_ID)
    code = area["code"]
    known_spans = build_known_spans(topology)
    residual = residual_spans(len(code), known_spans)

    byte_counts: Counter[int] = Counter()
    target_contexts: dict[int, list[dict]] = defaultdict(list)
    assumed_operand_counts: dict[int, Counter[str]] = {op: Counter() for op in TARGET_OPS}

    for span in residual:
        data = code[span["start"] : span["end"]]
        byte_counts.update(data)
        for rel, value in enumerate(data):
            offset = span["start"] + rel
            if value not in TARGET_OPS:
                continue
            window = code[offset : min(len(code), offset + 8)]
            before, after = neighbor_label(offset, known_spans)
            context = {
                "offset": offset,
                "offset_hex": f"0x{offset:04x}",
                "residual_span": f"0x{span['start']:04x}..0x{span['end']:04x}",
                "next_bytes": hex_bytes(window),
                "before": before,
                "after": after,
            }
            target_contexts[value].append(context)
            for length in (1, 2, 3, 4, 5):
                if offset + length <= len(code):
                    assumed_operand_counts[value][f"len{length}:{hex_bytes(code[offset:offset + length])}"] += 1

    result = {
        "schema": "joao_control_candidate_analysis_v1",
        "source_script": SCRIPT_ID,
        "summary": {
            "code_len": len(code),
            "known_span_count": len(known_spans),
            "residual_span_count": len(residual),
            "residual_bytes": sum(span["end"] - span["start"] for span in residual),
        },
        "residual_spans": [
            {
                "start": span["start"],
                "start_hex": f"0x{span['start']:04x}",
                "end": span["end"],
                "end_hex": f"0x{span['end']:04x}",
                "length": span["end"] - span["start"],
                "bytes": hex_bytes(code[span["start"] : span["end"]]),
            }
            for span in residual
        ],
        "top_residual_bytes": [{"byte": f"{value:02x}", "count": count} for value, count in byte_counts.most_common(80)],
        "targets": {
            f"{op:02x}": {
                "count": len(target_contexts[op]),
                "contexts": target_contexts[op],
                "top_forms": [
                    {"form": form, "count": count}
                    for form, count in assumed_operand_counts[op].most_common(24)
                ],
            }
            for op in TARGET_OPS
        },
    }
    (OUT_DIR / "joao_control_candidates.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# João Control Candidate Analysis",
        "",
        "This removes known long text motifs and short text motifs from `Snr1.chunk0.sub0`, then summarizes the remaining control-looking bytes.",
        "",
        f"- Code length: `{len(code)}`",
        f"- Known spans: `{len(known_spans)}`",
        f"- Residual spans: `{len(residual)}`",
        f"- Residual bytes: `{sum(span['end'] - span['start'] for span in residual)}`",
        "",
        "## Residual Spans",
        "",
    ]
    for span in result["residual_spans"]:
        lines.append(f"- `{span['start_hex']}..{span['end_hex']}` len={span['length']} bytes=`{span['bytes']}`")

    lines += ["", "## Top Residual Bytes", ""]
    for row in result["top_residual_bytes"][:32]:
        lines.append(f"- `{row['byte']}`: {row['count']}")

    lines += ["", "## Target Opcode Contexts", ""]
    for op in TARGET_OPS:
        target = result["targets"][f"{op:02x}"]
        lines += [f"### `{op:02x}`", "", f"- Count: `{target['count']}`", "", "Contexts:", ""]
        for context in target["contexts"][:40]:
            lines.append(
                f"- `{context['offset_hex']}` span={context['residual_span']} "
                f"next=`{context['next_bytes']}` before={context['before']} after={context['after']}"
            )
        lines += ["", "Top byte forms:", ""]
        for form in target["top_forms"][:12]:
            lines.append(f"- `{form['form']}`: {form['count']}")
        lines.append("")

    lines += ["## Initial Interpretation", ""]
    lines += [
        "- After removing long and short text motifs, residual bytes drop to the control layer around the text timeline.",
        "- `ad` and `ac` mostly appear as 4-byte-looking forms near segment boundaries, for example `ad 00 01 2a` and `ac 05 00 40`.",
        "- `fe 02 62` and `fe 07 48` look like compact control separators or calls with a 2-byte operand.",
        "- `f8` often appears immediately before `f2`, `ad`, or `fe`, so it is a high-priority branch/return modifier candidate.",
        "- The next disassembler pass should treat these as candidate lengths only, then test whether residual spans align cleanly.",
    ]
    (OUT_DIR / "joao_control_candidates.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'joao_control_candidates.json'}")
    print(f"Wrote {OUT_DIR / 'joao_control_candidates.md'}")


if __name__ == "__main__":
    main()
