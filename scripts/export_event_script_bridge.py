#!/usr/bin/env python3
"""Bridge the current topology events to script chunks for each storyline."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = ROOT / "output" / "game_topology" / "game_topology_bundle_v1.json"
SCRIPT_INDEX = ROOT / "output" / "sndt_topology" / "sndt_script_index_v1.json"
OUT_DIR = ROOT / "output" / "game_topology"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_bridge() -> dict:
    topology = load_json(TOPOLOGY)
    script_index = load_json(SCRIPT_INDEX)

    line_anchors = {
        "Snr1": ["Snr1.chunk0.sub0", "Snr1.chunk1.sub0", "Snr1.chunk3.sub0", "Snr1.chunk5.sub0"],
        "Snr2": ["Snr2.chunk0.sub0", "Snr2.chunk1.sub0", "Snr2.chunk6.sub3", "Snr2.chunk7.sub7"],
        "Snr3": ["Snr3.chunk0.sub0", "Snr3.chunk3.sub0", "Snr3.chunk4.sub3", "Snr3.chunk5.sub3"],
        "Snr4": ["Snr4.chunk0.sub0", "Snr4.chunk4.sub1", "Snr4.chunk4.sub3"],
        "Snr5": ["Snr5.chunk0.sub0", "Snr5.chunk2.sub1", "Snr5.chunk2.sub2", "Snr5.chunk3.sub2"],
        "Snr6": ["Snr6.chunk1.sub0", "Snr6.chunk2.sub4", "Snr6.chunk3.sub3", "Snr6.chunk4.sub0", "Snr6.chunk5.sub0"],
    }

    subscripts_by_id = {}
    for file_info in script_index["files"]:
        for chunk in file_info["chunks"]:
            for sub in chunk["subscripts"]:
                subscripts_by_id[sub["id"]] = {
                    "id": sub["id"],
                    "chunk": chunk["id"],
                    "index": sub["index"],
                    "dispatch_count": sub["dispatch_count"],
                    "text_ref_count": sub["text_ref_count"],
                    "first_text_refs": sub["first_text_refs"],
                }

    events_by_line: dict[str, list[dict]] = {}
    for event in topology["graphs"]["events"]["nodes"]:
        events_by_line.setdefault(event["line"], []).append(event)

    def choose_subscript_ids(line: str, event_index: int, event_count: int) -> list[str]:
        anchors = line_anchors.get(line, [])
        if not anchors:
            return []
        if event_count <= 1 or len(anchors) == 1:
            return anchors[:1]
        center = round(event_index * (len(anchors) - 1) / (event_count - 1))
        chosen = [anchors[center]]
        if center + 1 < len(anchors) and (event_index % 2 == 0 or len(anchors) < event_count):
            chosen.append(anchors[center + 1])
        elif center - 1 >= 0:
            chosen.insert(0, anchors[center - 1])
        return list(dict.fromkeys(chosen))

    def collect_evidence(sub_rows: list[dict]) -> list[dict]:
        seen: set[tuple[int, str]] = set()
        evidence: list[dict] = []
        for sub in sub_rows:
            for ref in sub.get("first_text_refs", []):
                key = (ref["text_id"], ref["text"])
                if key in seen:
                    continue
                seen.add(key)
                evidence.append(
                    {
                        "text_id": ref["text_id"],
                        "text": ref["text"],
                        "confidence": ref["confidence"],
                        "source_subscript": sub["id"],
                    }
                )
                if len(evidence) >= 8:
                    return evidence
        return evidence

    rows = []
    for line, events in events_by_line.items():
        for index, event in enumerate(events):
            sub_ids = choose_subscript_ids(line, index, len(events))
            sub_rows = [subscripts_by_id[sid] for sid in sub_ids if sid in subscripts_by_id]
            evidence = collect_evidence(sub_rows)
            rows.append(
                {
                    "event_id": event["id"],
                    "event_label": event["label"],
                    "line": line,
                    "state_before": event["state_before"],
                    "state_after": event["state_after"],
                    "actors": event["actors"],
                    "locations": event["locations"],
                    "subscript_ids": sub_ids,
                    "subscripts": sub_rows,
                    "evidence": evidence,
                    "dispatch_total": sum(sub["dispatch_count"] for sub in sub_rows),
                    "text_ref_total": sum(sub["text_ref_count"] for sub in sub_rows),
                }
            )

    lines = {
        "schema": "sea2_event_script_bridge_v1",
        "source": {
            "topology": str(TOPOLOGY.relative_to(ROOT)),
            "script_index": str(SCRIPT_INDEX.relative_to(ROOT)),
            "line_anchors": line_anchors,
            "alignment_note": "Event rows are aligned to the nearest anchor subscript(s) by position within each storyline, not runtime-confirmed traces.",
        },
        "events": rows,
    }

    return lines


def build_report(bridge: dict) -> str:
    lines = [
        "# Event Script Bridge Report",
        "",
        f"- schema: `{bridge['schema']}`",
        f"- topology: `{bridge['source']['topology']}`",
        f"- script_index: `{bridge['source']['script_index']}`",
        f"- alignment_note: {bridge['source']['alignment_note']}",
        f"- events: {len(bridge['events'])}",
        "",
        "## Event Coverage",
    ]
    for row in bridge["events"]:
        lines.append(
            f"- {row['event_id']} {row['event_label']} | {row['line']} | "
            f"subscripts={','.join(row['subscript_ids'])} | dispatch={row['dispatch_total']} | "
            f"text_refs={row['text_ref_total']} | actors={','.join(row['actors'])}"
        )
        for ref in row["evidence"][:3]:
            snippet = ref["text"].replace("\n", " / ")
            lines.append(f"  - {ref['source_subscript']} | text#{ref['text_id']}: {snippet}")
    return "\n".join(lines) + "\n"


def main() -> None:
    bridge = build_bridge()
    json_path = OUT_DIR / "event_script_bridge_v1.json"
    md_path = OUT_DIR / "event_script_bridge_v1.md"
    json_path.write_text(json.dumps(bridge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(bridge), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
