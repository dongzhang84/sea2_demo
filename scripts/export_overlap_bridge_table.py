#!/usr/bin/env python3
"""Export a concise bridge table from the distinctive overlap graph."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "output" / "game_topology" / "event_overlap_graph_v1.json"
TEXT_INDEX = ROOT / "output" / "game_topology" / "event_text_index_v1.json"
OUT_DIR = ROOT / "output" / "game_topology"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_table() -> dict:
    graph = load_json(GRAPH)
    text_index = load_json(TEXT_INDEX)
    text_by_id = {entry["text_id"]: entry["text"] for entry in text_index["texts"]}

    line_pairs = defaultdict(list)
    for edge in graph["distinctive_line_edges"]:
        key = tuple(sorted((edge["from"], edge["to"])))
        line_pairs[key].append(edge)

    rows = []
    for (left, right), edges in sorted(line_pairs.items()):
        all_shared = sorted({text_id for edge in edges for text_id in edge["shared_text_ids"]})
        rows.append(
            {
                "from": left,
                "to": right,
                "bridge_count": len(edges),
                "shared_text_ids": all_shared,
                "shared_texts": [
                    {
                        "text_id": text_id,
                        "text": text_by_id.get(text_id, ""),
                    }
                    for text_id in all_shared
                ],
                "top_event_bridges": [
                    {
                        "from": edge["from"],
                        "to": edge["to"],
                        "weight": edge["weight"],
                        "shared_text_ids": edge["shared_text_ids"],
                        "shared_texts": [
                            {"text_id": text_id, "text": text_by_id.get(text_id, "")}
                            for text_id in edge["shared_text_ids"]
                        ],
                    }
                    for edge in edges[:6]
                ],
            }
        )

    return {
        "schema": "sea2_overlap_bridge_table_v1",
        "source": {
            "graph": str(GRAPH.relative_to(ROOT)),
            "text_index": str(TEXT_INDEX.relative_to(ROOT)),
        },
        "bridge_rows": rows,
    }


def build_report(table: dict) -> str:
    lines = [
        "# Overlap Bridge Table",
        "",
        f"- schema: `{table['schema']}`",
        f"- graph: `{table['source']['graph']}`",
        f"- text_index: `{table['source']['text_index']}`",
        "",
    ]
    for row in table["bridge_rows"]:
        texts = " | ".join(
            f"#{item['text_id']}: {item['text'].replace(chr(10), ' / ')}"
            for item in row["shared_texts"][:6]
        )
        lines.append(
            f"- {row['from']} <-> {row['to']} | bridges={row['bridge_count']} | shared={texts}"
        )
        for edge in row["top_event_bridges"][:3]:
            shared = " | ".join(
                f"#{item['text_id']}: {item['text'].replace(chr(10), ' / ')}"
                for item in edge["shared_texts"][:4]
            )
            lines.append(f"  - {edge['from']} <-> {edge['to']} | weight={edge['weight']} | {shared}")
    return "\n".join(lines) + "\n"


def main() -> None:
    table = build_table()
    json_path = OUT_DIR / "overlap_bridge_table_v1.json"
    md_path = OUT_DIR / "overlap_bridge_table_v1.md"
    json_path.write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(table), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
