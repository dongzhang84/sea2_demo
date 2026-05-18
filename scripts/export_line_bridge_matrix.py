#!/usr/bin/env python3
"""Export a pairwise bridge matrix between the six storylines."""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = ROOT / "output" / "game_topology" / "game_topology_bundle_v1.json"
OUT_DIR = ROOT / "output" / "game_topology"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_matrix() -> dict:
    topology = load_json(TOPOLOGY)

    line_labels = {node["id"]: node["label"] for node in topology["graphs"]["storylines"]["nodes"]}

    line_events: dict[str, list[dict]] = defaultdict(list)
    for event in topology["graphs"]["events"]["nodes"]:
        line_events[event["line"]].append(event)

    line_actors: dict[str, set[str]] = defaultdict(set)
    line_locations: dict[str, set[str]] = defaultdict(set)
    line_states: dict[str, set[str]] = defaultdict(set)
    line_event_ids: dict[str, set[str]] = defaultdict(set)

    for event in topology["graphs"]["events"]["nodes"]:
        line = event["line"]
        line_event_ids[line].add(event["id"])
        line_actors[line].update(event.get("actors", []))
        line_locations[line].update(event.get("locations", []))
        line_states[line].add(event.get("state_before"))
        line_states[line].add(event.get("state_after"))

    rows = []
    for left, right in combinations(sorted(line_labels), 2):
        shared_actors = sorted(line_actors[left] & line_actors[right])
        shared_locations = sorted(line_locations[left] & line_locations[right])
        shared_states = sorted(line_states[left] & line_states[right])
        shared_events = sorted(line_event_ids[left] & line_event_ids[right])
        score = len(shared_actors) * 4 + len(shared_locations) * 3 + len(shared_states) * 2 + len(shared_events) * 6
        rows.append(
            {
                "from": left,
                "to": right,
                "from_label": line_labels[left],
                "to_label": line_labels[right],
                "shared_actors": shared_actors,
                "shared_locations": shared_locations,
                "shared_states": shared_states,
                "shared_event_ids": shared_events,
                "score": score,
            }
        )

    rows.sort(key=lambda item: (-item["score"], item["from"], item["to"]))

    return {
        "schema": "sea2_line_bridge_matrix_v1",
        "source": {
            "topology": str(TOPOLOGY.relative_to(ROOT)),
        },
        "lines": [
            {"id": line_id, "label": line_labels[line_id]} for line_id in sorted(line_labels)
        ],
        "bridge_rows": rows,
    }


def build_report(matrix: dict) -> str:
    lines = [
        "# Line Bridge Matrix",
        "",
        f"- schema: `{matrix['schema']}`",
        f"- source: `{matrix['source']['topology']}`",
        "",
        "## Bridges",
    ]
    for row in matrix["bridge_rows"]:
        actors = ", ".join(row["shared_actors"]) or "-"
        locations = ", ".join(row["shared_locations"]) or "-"
        states = ", ".join(row["shared_states"]) or "-"
        lines.append(
            f"- {row['from']} <-> {row['to']} | score={row['score']} | actors={actors} | locations={locations} | states={states}"
        )
    return "\n".join(lines) + "\n"


def write_mermaid(matrix: dict) -> Path:
    lines = [
        "flowchart LR",
    ]
    for line in matrix["lines"]:
        node = line["id"]
        label = line["label"].replace('"', "'")
        lines.append(f'  {node}["{label}"]')
    for row in matrix["bridge_rows"]:
        if row["score"] < 6:
            continue
        parts = []
        if row["shared_actors"]:
            parts.append(f"A:{len(row['shared_actors'])}")
        if row["shared_locations"]:
            parts.append(f"L:{len(row['shared_locations'])}")
        if row["shared_states"]:
            parts.append(f"S:{len(row['shared_states'])}")
        if row["shared_event_ids"]:
            parts.append(f"E:{len(row['shared_event_ids'])}")
        label = " / ".join(parts) if parts else str(row["score"])
        lines.append(f'  {row["from"]} -->|{label}| {row["to"]}')
    path = OUT_DIR / "line_bridge_matrix_v1.mmd"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> None:
    matrix = build_matrix()
    json_path = OUT_DIR / "line_bridge_matrix_v1.json"
    md_path = OUT_DIR / "line_bridge_matrix_v1.md"
    mmd_path = write_mermaid(matrix)
    json_path.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(matrix), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {mmd_path}")


if __name__ == "__main__":
    main()
