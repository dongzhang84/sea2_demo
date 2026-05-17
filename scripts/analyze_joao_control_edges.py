#!/usr/bin/env python3
"""Analyze candidate control-flow edges in the Joao opening script.

This is intentionally conservative: it tests several plausible integer
interpretations for control operands and reports which ones land on, inside, or
near known topology timeline items.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISASM_PATH = ROOT / "output/sndt_analysis/joao_control_disasm.json"
TOPOLOGY_PATH = ROOT / "output/sndt_topology/joao_opening_topology.json"
OUT_JSON = ROOT / "output/sndt_analysis/joao_control_edges.json"
OUT_MD = ROOT / "output/sndt_analysis/joao_control_edges.md"

CONTROL_OPS = {"ad_control", "ac_control", "8c_control", "fe_control"}
NEAR_DISTANCE = 4


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def hex4(value: int | None) -> str | None:
    if value is None:
        return None
    return f"0x{value:04x}"


def parse_bytes(raw_text: str) -> list[int]:
    return [int(part, 16) for part in raw_text.split()]


def be_int(values: list[int]) -> int:
    out = 0
    for value in values:
        out = (out << 8) | value
    return out


def le_int(values: list[int]) -> int:
    out = 0
    for shift, value in enumerate(values):
        out |= value << (shift * 8)
    return out


def operand_candidates(op: str, raw: list[int]) -> list[dict]:
    if len(raw) <= 1:
        return []

    body = raw[1:]
    candidates = [
        {"name": "operand_be", "target": be_int(body), "bytes": body},
        {"name": "operand_le", "target": le_int(body), "bytes": body},
    ]

    if len(body) >= 2:
        candidates.extend(
            [
                {"name": "low16_be", "target": be_int(body[-2:]), "bytes": body[-2:]},
                {"name": "low16_le", "target": le_int(body[-2:]), "bytes": body[-2:]},
                {"name": "high16_be", "target": be_int(body[:2]), "bytes": body[:2]},
                {"name": "high16_le", "target": le_int(body[:2]), "bytes": body[:2]},
            ]
        )

    if len(body) >= 3:
        candidates.extend(
            [
                {"name": "low24_be", "target": be_int(body[-3:]), "bytes": body[-3:]},
                {"name": "low24_le", "target": le_int(body[-3:]), "bytes": body[-3:]},
            ]
        )

    seen = set()
    unique = []
    for candidate in candidates:
        key = (candidate["name"], candidate["target"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
    return unique


def flatten_instructions(disasm: dict) -> list[dict]:
    instructions = []
    for span in disasm["spans"]:
        for ins in span["instructions"]:
            copy = dict(ins)
            copy["span_start"] = span["start"]
            copy["span_end"] = span["end"]
            instructions.append(copy)
    return sorted(instructions, key=lambda item: item["offset"])


def classify_target(target: int, timeline: list[dict], code_len: int) -> dict:
    if target < 0:
        in_code = False
    else:
        in_code = target < code_len

    exact_start = [item for item in timeline if item["start"] == target]
    exact_end = [item for item in timeline if item["end"] == target]
    inside = [item for item in timeline if item["start"] <= target < item["end"]]

    boundaries = []
    for item in timeline:
        boundaries.append(("start", item, item["start"], abs(target - item["start"])))
        boundaries.append(("end", item, item["end"], abs(target - item["end"])))
    nearest_kind, nearest_item, nearest_offset, nearest_distance = min(
        boundaries, key=lambda row: row[3]
    )

    if exact_start:
        match = "exact_start"
        item = exact_start[0]
    elif exact_end:
        match = "exact_end"
        item = exact_end[0]
    elif inside:
        match = "inside_item"
        item = inside[0]
    elif nearest_distance <= NEAR_DISTANCE:
        match = "near_item"
        item = nearest_item
    else:
        match = "no_match"
        item = None

    return {
        "target": target,
        "target_hex": hex4(target),
        "in_code_range": in_code,
        "match": match,
        "item": summarize_item(item),
        "nearest": {
            "boundary": nearest_kind,
            "offset": nearest_offset,
            "offset_hex": hex4(nearest_offset),
            "distance": nearest_distance,
            "item": summarize_item(nearest_item),
        },
    }


def summarize_item(item: dict | None) -> dict | None:
    if item is None:
        return None
    summary = {
        "id": item["id"],
        "kind": item["kind"],
        "start": item["start"],
        "start_hex": item["start_hex"],
        "end": item["end"],
        "end_hex": item["end_hex"],
        "title": item.get("title"),
    }
    if "text_range" in item:
        summary["text_range"] = item["text_range"]
    if "text_id" in item:
        summary["text_id"] = item["text_id"]
    return summary


def confidence_rank(match: str) -> int:
    return {
        "exact_start": 5,
        "exact_end": 4,
        "inside_item": 3,
        "near_item": 2,
        "no_match": 0,
    }[match]


def candidate_prior(op: str, candidate_name: str) -> int:
    """Prefer operand forms that look like actual script pointers.

    The first operand byte in ad/ac/8c often behaves like a slot/group selector,
    so raw high16 matches are more likely to be accidental than a big-endian
    low16 or whole big-endian operand that lands near executable text.
    """
    if op in {"ad_control", "ac_control"}:
        priorities = {
            "operand_be": 90,
            "low24_be": 85,
            "low16_be": 80,
            "high16_be": 30,
            "high16_le": 20,
            "low16_le": 10,
            "operand_le": 5,
            "low24_le": 5,
        }
    elif op == "8c_control":
        priorities = {
            "low16_be": 90,
            "operand_be": 70,
            "low24_be": 65,
            "high16_be": 25,
            "high16_le": 20,
            "low16_le": 10,
            "operand_le": 5,
            "low24_le": 5,
        }
    else:
        priorities = {
            "operand_be": 90,
            "low16_be": 90,
            "high16_be": 70,
            "operand_le": 5,
            "low16_le": 5,
            "high16_le": 5,
        }
    return priorities.get(candidate_name, 0)


def edge_score(edge: dict) -> tuple[int, int, int, int]:
    return (
        confidence_rank(edge["match"]),
        1 if edge["in_code_range"] else 0,
        candidate_prior(edge["source_op"], edge["candidate"]),
        -edge["nearest"]["distance"],
    )


def analyze() -> dict:
    disasm = load_json(DISASM_PATH)
    topology = load_json(TOPOLOGY_PATH)
    timeline = sorted(topology["timeline"], key=lambda item: item["start"])
    code_len = max(
        [item["end"] for item in timeline]
        + [span["end"] for span in disasm["spans"]]
    )

    edges = []
    summary_by_op_candidate = defaultdict(Counter)
    preferred_by_instruction = []

    for ins in flatten_instructions(disasm):
        op = ins["op"]
        if op not in CONTROL_OPS:
            continue
        raw = parse_bytes(ins["bytes"])
        instruction_edges = []
        for candidate in operand_candidates(op, raw):
            classified = classify_target(candidate["target"], timeline, code_len)
            edge = {
                "source_offset": ins["offset"],
                "source_offset_hex": ins["offset_hex"],
                "source_op": op,
                "source_bytes": ins["bytes"],
                "candidate": candidate["name"],
                "candidate_bytes": " ".join(f"{b:02x}" for b in candidate["bytes"]),
                **classified,
            }
            edges.append(edge)
            instruction_edges.append(edge)
            bucket = f"{op}:{candidate['name']}"
            summary_by_op_candidate[bucket]["total"] += 1
            summary_by_op_candidate[bucket][classified["match"]] += 1
            if classified["in_code_range"]:
                summary_by_op_candidate[bucket]["in_code_range"] += 1

        if instruction_edges:
            best = max(
                instruction_edges,
                key=edge_score,
            )
            preferred_by_instruction.append(best)

    match_counts = Counter(edge["match"] for edge in edges)
    preferred_counts = Counter(edge["match"] for edge in preferred_by_instruction)

    return {
        "schema": "joao_control_edges_v1",
        "source_script": topology["source_script"],
        "inputs": {
            "disasm": str(DISASM_PATH.relative_to(ROOT)),
            "topology": str(TOPOLOGY_PATH.relative_to(ROOT)),
        },
        "summary": {
            "code_len": code_len,
            "code_len_hex": hex4(code_len),
            "timeline_items": len(timeline),
            "control_instructions": len(preferred_by_instruction),
            "candidate_edges": len(edges),
            "match_counts": dict(match_counts),
            "preferred_match_counts": dict(preferred_counts),
        },
        "summary_by_op_candidate": {
            key: dict(counter) for key, counter in sorted(summary_by_op_candidate.items())
        },
        "preferred_by_instruction": preferred_by_instruction,
        "edges": edges,
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# Joao Opening Control Edge Candidates",
        "",
        "This report tests whether control operands in the Joao opening subscript point at known timeline byte ranges.",
        "",
        "## Summary",
        "",
    ]
    summary = report["summary"]
    for key in [
        "code_len_hex",
        "timeline_items",
        "control_instructions",
        "candidate_edges",
    ]:
        lines.append(f"- {key}: {summary[key]}")
    lines.append(f"- match_counts: `{summary['match_counts']}`")
    lines.append(f"- preferred_match_counts: `{summary['preferred_match_counts']}`")
    lines.append("")

    lines.extend(
        [
            "## Candidate Interpretation Scores",
            "",
            "| op:candidate | total | in range | exact start | exact end | inside | near | none |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for key, counts in report["summary_by_op_candidate"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    key,
                    str(counts.get("total", 0)),
                    str(counts.get("in_code_range", 0)),
                    str(counts.get("exact_start", 0)),
                    str(counts.get("exact_end", 0)),
                    str(counts.get("inside_item", 0)),
                    str(counts.get("near_item", 0)),
                    str(counts.get("no_match", 0)),
                ]
            )
            + " |"
        )
    lines.append("")

    lines.extend(
        [
            "## Preferred Edge Interpretations",
            "",
            "Preferred interpretations bias toward big-endian operand/low16 forms that look like script pointers. Near matches are kept because some operands may point to the byte just before a text motif or to a small control prelude.",
            "",
            "| source | bytes | preferred candidate | target | match | timeline item | nearest |",
            "|---|---|---|---:|---|---|---|",
        ]
    )
    for edge in report["preferred_by_instruction"]:
        item = edge["item"] or edge["nearest"]["item"]
        item_label = ""
        if item:
            label_bits = [item["id"], item["kind"]]
            if item.get("text_range") is not None:
                label_bits.append(f"text={item['text_range']}")
            elif item.get("text_id") is not None:
                label_bits.append(f"text={item['text_id']}")
            if item.get("title"):
                label_bits.append(str(item["title"]))
            item_label = " / ".join(label_bits)
        nearest = edge["nearest"]
        nearest_label = (
            f"{nearest['boundary']} {nearest['offset_hex']} d={nearest['distance']}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{edge['source_offset_hex']} {edge['source_op']}",
                    edge["source_bytes"],
                    edge["candidate"],
                    edge["target_hex"],
                    edge["match"],
                    item_label,
                    nearest_label,
                ]
            )
            + " |"
        )
    lines.append("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = analyze()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
