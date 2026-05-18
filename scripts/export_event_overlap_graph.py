#!/usr/bin/env python3
"""Export overlap graphs derived from the event text index."""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "output" / "game_topology" / "event_text_index_v1.json"
OUT_DIR = ROOT / "output" / "game_topology"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_overlap_graph() -> dict:
    index = load_json(INDEX)
    events = []
    event_texts: dict[str, set[int]] = {}
    event_line: dict[str, str] = {}
    text_event_counts: dict[int, int] = {}

    for entry in index["texts"]:
        text_event_counts[entry["text_id"]] = len(entry["event_ids"])
    distinctive_texts = {text_id for text_id, count in text_event_counts.items() if count <= 8}

    for line, rows in index["events_by_line"].items():
        for row in rows:
            events.append(row["event_id"])
            event_line[row["event_id"]] = line
            event_texts[row["event_id"]] = set(row["ranked_text_ids"])

    event_edges = []
    distinctive_event_edges = []
    for left, right in combinations(events, 2):
        shared = sorted(event_texts[left] & event_texts[right])
        if not shared:
            continue
        event_edges.append(
            {
                "from": left,
                "to": right,
                "weight": len(shared),
                "shared_text_ids": shared,
            }
        )
        distinctive_shared = sorted((event_texts[left] & event_texts[right]) & distinctive_texts)
        if distinctive_shared:
            distinctive_event_edges.append(
                {
                    "from": left,
                    "to": right,
                    "weight": len(distinctive_shared),
                    "shared_text_ids": distinctive_shared,
                }
            )

    line_texts: dict[str, set[int]] = defaultdict(set)
    for event_id, texts in event_texts.items():
        line_texts[event_line[event_id]].update(texts)

    line_edges = []
    distinctive_line_edges = []
    for left, right in combinations(sorted(line_texts), 2):
        shared = sorted(line_texts[left] & line_texts[right])
        if not shared:
            continue
        line_edges.append(
            {
                "from": left,
                "to": right,
                "weight": len(shared),
                "shared_text_ids": shared,
            }
        )
        distinctive_shared = sorted((line_texts[left] & line_texts[right]) & distinctive_texts)
        if distinctive_shared:
            distinctive_line_edges.append(
                {
                    "from": left,
                    "to": right,
                    "weight": len(distinctive_shared),
                    "shared_text_ids": distinctive_shared,
                }
            )

    event_edges.sort(key=lambda item: (-item["weight"], item["from"], item["to"]))
    distinctive_event_edges.sort(key=lambda item: (-item["weight"], item["from"], item["to"]))
    line_edges.sort(key=lambda item: (-item["weight"], item["from"], item["to"]))
    distinctive_line_edges.sort(key=lambda item: (-item["weight"], item["from"], item["to"]))

    clusters = []
    for row in sorted(
        (
            {
                "event_id": event_id,
                "line": event_line[event_id],
                "text_count": len(texts),
                "shared_with": sum(1 for other in events if other != event_id and (event_texts[event_id] & event_texts[other])),
            }
            for event_id, texts in event_texts.items()
        ),
        key=lambda item: (-item["shared_with"], item["line"], item["event_id"]),
    ):
        clusters.append(row)

    return {
        "schema": "sea2_event_overlap_graph_v1",
        "source": {
            "event_text_index": str(INDEX.relative_to(ROOT)),
        },
        "summary": {
            "event_count": len(events),
            "event_edge_count": len(event_edges),
            "line_edge_count": len(line_edges),
            "distinctive_event_edge_count": len(distinctive_event_edges),
            "distinctive_line_edge_count": len(distinctive_line_edges),
        },
        "event_nodes": [
            {
                "event_id": event_id,
                "line": event_line[event_id],
                "text_count": len(event_texts[event_id]),
            }
            for event_id in events
        ],
        "event_edges": event_edges,
        "distinctive_event_edges": distinctive_event_edges,
        "line_edges": line_edges,
        "distinctive_line_edges": distinctive_line_edges,
        "event_clusters": clusters,
        "distinctive_text_ids": sorted(distinctive_texts),
    }


def build_report(graph: dict) -> str:
    lines = [
        "# Event Overlap Graph",
        "",
        f"- schema: `{graph['schema']}`",
        f"- source: `{graph['source']['event_text_index']}`",
        f"- events: {graph['summary']['event_count']}",
        f"- event_edges: {graph['summary']['event_edge_count']}",
        f"- line_edges: {graph['summary']['line_edge_count']}",
        f"- distinctive_event_edges: {graph['summary']['distinctive_event_edge_count']}",
        f"- distinctive_line_edges: {graph['summary']['distinctive_line_edge_count']}",
        "",
        "## Top Distinctive Event Overlaps",
    ]
    for edge in graph["distinctive_event_edges"][:30]:
        shared = ", ".join(f"#{text_id}" for text_id in edge["shared_text_ids"][:8])
        lines.append(f"- {edge['from']} <-> {edge['to']} | weight={edge['weight']} | shared={shared}")
    lines.append("")
    lines.append("## Distinctive Line Overlaps")
    for edge in graph["distinctive_line_edges"]:
        shared = ", ".join(f"#{text_id}" for text_id in edge["shared_text_ids"][:8])
        lines.append(f"- {edge['from']} <-> {edge['to']} | weight={edge['weight']} | shared={shared}")
    lines.append("")
    lines.append("## Event Hotspots")
    for row in graph["event_clusters"][:33]:
        lines.append(
            f"- {row['event_id']} | {row['line']} | shared_with={row['shared_with']} | text_count={row['text_count']}"
        )
    return "\n".join(lines) + "\n"


def write_dot(graph: dict) -> Path:
    lines = [
        "graph event_overlap_graph_v1 {",
        '  graph [rankdir="LR", bgcolor="white"];',
        '  node [shape="box", style="rounded,filled", fillcolor="#f3f4ff", color="#c7caf6", fontname="Arial"];',
        '  edge [color="#7b7f9a", penwidth=1.2];',
    ]
    for row in graph["event_nodes"]:
        lines.append(f'  "{row["event_id"]}" [label="{row["event_id"]}\\n{row["line"]}\\ntexts={row["text_count"]}"];')
    for edge in graph["event_edges"][:80]:
        if edge["weight"] < 2:
            continue
        lines.append(
            f'  "{edge["from"]}" -- "{edge["to"]}" [label="{edge["weight"]}"];'
        )
    lines.append("}")
    dot_path = OUT_DIR / "event_overlap_graph_v1.dot"
    dot_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dot_path


def write_line_mermaid(graph: dict) -> Path:
    lines = [
        "flowchart LR",
        '  Snr1["Snr1"]',
        '  Snr2["Snr2"]',
        '  Snr3["Snr3"]',
        '  Snr4["Snr4"]',
        '  Snr5["Snr5"]',
        '  Snr6["Snr6"]',
    ]
    for edge in graph["distinctive_line_edges"]:
        if edge["weight"] < 2:
            continue
        label = f"{edge['weight']} shared"
        lines.append(f'  {edge["from"]} -->|{label}| {edge["to"]}')
    path = OUT_DIR / "line_overlap_graph_v1.mmd"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    graph = build_overlap_graph()
    json_path = OUT_DIR / "event_overlap_graph_v1.json"
    md_path = OUT_DIR / "event_overlap_graph_v1.md"
    mmd_path = write_line_mermaid(graph)
    json_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(graph), encoding="utf-8")
    dot_path = write_dot(graph)
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {mmd_path}")
    print(f"Wrote {dot_path}")


if __name__ == "__main__":
    main()
