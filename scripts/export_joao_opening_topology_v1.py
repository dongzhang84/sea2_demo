#!/usr/bin/env python3
"""Export a first control-edge topology for the Joao opening script."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY_PATH = ROOT / "output/sndt_topology/joao_opening_topology.json"
DISASM_PATH = ROOT / "output/sndt_analysis/joao_control_disasm.json"
EDGES_PATH = ROOT / "output/sndt_analysis/joao_control_edges.json"
OUT_JSON = ROOT / "output/sndt_topology/joao_opening_topology_v1.json"
OUT_DOT = ROOT / "output/sndt_topology/joao_opening_topology_v1.dot"
OUT_MD = ROOT / "docs/SNDT_JOAO_OPENING_TOPOLOGY_V1.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def confidence(match: str) -> str:
    return {
        "exact_start": "high",
        "exact_end": "high",
        "inside_item": "medium",
        "near_item": "low",
    }.get(match, "none")


def node_id_for_item(item: dict) -> str:
    return item["id"]


def span_node_id(span: dict) -> str:
    return f"control_span_{span['start_hex']}_{span['end_hex']}"


def summarize_item(item: dict) -> str:
    if item.get("title"):
        title = item["title"]
    elif item.get("text_id") is not None:
        title = f"text {item['text_id']}"
    elif item.get("text_range") is not None:
        title = f"text {item['text_range']}"
    else:
        title = item["id"]
    return str(title)


def build_nodes(base: dict, disasm: dict) -> tuple[list[dict], dict[str, str]]:
    nodes = []
    offset_to_node = {}

    for item in base["timeline"]:
        node = {
            "id": node_id_for_item(item),
            "kind": item["kind"],
            "start": item["start"],
            "start_hex": item["start_hex"],
            "end": item["end"],
            "end_hex": item["end_hex"],
            "label": summarize_item(item),
            "text_range": item.get("text_range"),
            "text_id": item.get("text_id"),
            "source": item,
        }
        nodes.append(node)
        for offset in range(item["start"], item["end"]):
            offset_to_node[offset] = node["id"]

    for span in disasm["spans"]:
        op_counts = Counter(ins["op"] for ins in span["instructions"])
        node = {
            "id": span_node_id(span),
            "kind": "control_span",
            "start": span["start"],
            "start_hex": span["start_hex"],
            "end": span["end"],
            "end_hex": span["end_hex"],
            "label": f"control {span['start_hex']}-{span['end_hex']}",
            "instruction_count": len(span["instructions"]),
            "unknown_bytes": span["unknown_bytes"],
            "op_counts": dict(op_counts),
        }
        nodes.append(node)
        for offset in range(span["start"], span["end"]):
            offset_to_node.setdefault(offset, node["id"])

    return sorted(nodes, key=lambda item: (item["start"], item["end"], item["id"])), offset_to_node


def target_node(edge: dict) -> tuple[str | None, str | None]:
    if edge["match"] == "no_match":
        return None, None
    item = edge.get("item") or edge["nearest"].get("item")
    if not item:
        return None, None
    edge_type = "candidate_control"
    if edge["match"] == "near_item":
        edge_type = "near_control"
    return item["id"], edge_type


def build_edges(nodes: list[dict], offset_to_node: dict[str, str], edge_report: dict) -> list[dict]:
    edges = []
    ordered = sorted(nodes, key=lambda item: (item["start"], item["end"], item["id"]))
    for idx, node in enumerate(ordered[:-1]):
        nxt = ordered[idx + 1]
        edges.append(
            {
                "id": f"seq_{idx:03d}",
                "type": "sequence",
                "from": node["id"],
                "to": nxt["id"],
                "confidence": "structural",
            }
        )

    control_idx = 0
    for raw_edge in edge_report["preferred_by_instruction"]:
        dst, edge_type = target_node(raw_edge)
        if not dst:
            continue
        src = offset_to_node.get(raw_edge["source_offset"])
        if not src:
            continue
        edges.append(
            {
                "id": f"ctrl_{control_idx:03d}",
                "type": edge_type,
                "from": src,
                "to": dst,
                "confidence": confidence(raw_edge["match"]),
                "match": raw_edge["match"],
                "source_offset": raw_edge["source_offset"],
                "source_offset_hex": raw_edge["source_offset_hex"],
                "opcode": raw_edge["source_op"],
                "raw_bytes": raw_edge["source_bytes"],
                "target_offset": raw_edge["target"],
                "target_offset_hex": raw_edge["target_hex"],
                "candidate": raw_edge["candidate"],
                "nearest_distance": raw_edge["nearest"]["distance"],
            }
        )
        control_idx += 1

    return edges


def dot_quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def write_dot(nodes: list[dict], edges: list[dict]) -> None:
    lines = [
        "digraph joao_opening_topology_v1 {",
        "  rankdir=LR;",
        "  graph [fontname=\"Helvetica\"];",
        "  node [fontname=\"Helvetica\", shape=box, style=\"rounded,filled\", fillcolor=\"#f8f8f8\"];",
        "  edge [fontname=\"Helvetica\"];",
    ]
    for node in nodes:
        if node["kind"] == "control_span":
            fill = "#eef2ff"
        elif node["kind"] == "short_text":
            fill = "#f0fdf4"
        else:
            fill = "#fff7ed"
        label = f"{node['id']}\\n{node['start_hex']}-{node['end_hex']}\\n{node['label']}"
        lines.append(
            f"  {dot_quote(node['id'])} [label={dot_quote(label)}, fillcolor={dot_quote(fill)}];"
        )

    for edge in edges:
        if edge["type"] == "sequence":
            color = "#bbbbbb"
            style = "dotted"
            label = "seq"
        elif edge["type"] == "near_control":
            color = "#f59e0b"
            style = "dashed"
            label = f"{edge['opcode']} {edge['raw_bytes']} near"
        else:
            color = "#dc2626" if edge["confidence"] == "high" else "#2563eb"
            style = "solid"
            label = f"{edge['opcode']} {edge['raw_bytes']} {edge['match']}"
        lines.append(
            f"  {dot_quote(edge['from'])} -> {dot_quote(edge['to'])} "
            f"[label={dot_quote(label)}, color={dot_quote(color)}, style={dot_quote(style)}];"
        )
    lines.append("}")
    OUT_DOT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(report: dict) -> None:
    s = report["summary"]
    lines = [
        "# João Opening Topology v1",
        "",
        "This is the first João-opening topology export that includes candidate control-flow edges.",
        "",
        "## Summary",
        "",
        f"- nodes: {s['node_count']}",
        f"- sequence_edges: {s['sequence_edges']}",
        f"- candidate_control_edges: {s['candidate_control_edges']}",
        f"- near_control_edges: {s['near_control_edges']}",
        f"- high_confidence_control_edges: {s['high_confidence_control_edges']}",
        f"- medium_confidence_control_edges: {s['medium_confidence_control_edges']}",
        f"- low_confidence_control_edges: {s['low_confidence_control_edges']}",
        "",
        "## Interpretation",
        "",
        "The graph is still a candidate execution topology, not a fully runtime-confirmed VM trace. The important shift is that João opening now has explicit non-sequence edges derived from `ad/ac/8c/fe` operands.",
        "",
        "High confidence means the operand lands exactly on a known timeline start/end. Medium means it lands inside a known timeline item. Low means it is within four bytes of a known boundary.",
        "",
        "## Files",
        "",
        f"- `{OUT_JSON.relative_to(ROOT)}`",
        f"- `{OUT_DOT.relative_to(ROOT)}`",
        f"- `{EDGES_PATH.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    base = load_json(TOPOLOGY_PATH)
    disasm = load_json(DISASM_PATH)
    edge_report = load_json(EDGES_PATH)

    nodes, offset_to_node = build_nodes(base, disasm)
    edges = build_edges(nodes, offset_to_node, edge_report)

    edge_counts = Counter(edge["type"] for edge in edges)
    confidence_counts = Counter(
        edge.get("confidence") for edge in edges if edge["type"] != "sequence"
    )
    report = {
        "schema": "joao_opening_topology_v1",
        "source_script": base["source_script"],
        "inputs": {
            "timeline": str(TOPOLOGY_PATH.relative_to(ROOT)),
            "control_disasm": str(DISASM_PATH.relative_to(ROOT)),
            "control_edges": str(EDGES_PATH.relative_to(ROOT)),
        },
        "summary": {
            "node_count": len(nodes),
            "timeline_nodes": len(base["timeline"]),
            "control_span_nodes": len(disasm["spans"]),
            "edge_count": len(edges),
            "sequence_edges": edge_counts.get("sequence", 0),
            "candidate_control_edges": edge_counts.get("candidate_control", 0),
            "near_control_edges": edge_counts.get("near_control", 0),
            "high_confidence_control_edges": confidence_counts.get("high", 0),
            "medium_confidence_control_edges": confidence_counts.get("medium", 0),
            "low_confidence_control_edges": confidence_counts.get("low", 0),
        },
        "nodes": nodes,
        "edges": edges,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_dot(nodes, edges)
    write_report(report)
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_DOT.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
