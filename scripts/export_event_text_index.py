#!/usr/bin/env python3
"""Export a reverse index from script text evidence to topology events."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "output" / "game_topology" / "event_script_bridge_v1.json"
OUT_DIR = ROOT / "output" / "game_topology"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_index() -> dict:
    bridge = load_json(BRIDGE)

    texts_by_id: dict[int, dict] = {}
    events_by_line: dict[str, list[dict]] = defaultdict(list)

    for event in bridge["events"]:
        events_by_line[event["line"]].append(event)
        for evidence in event.get("evidence", []):
            text_id = evidence["text_id"]
            entry = texts_by_id.setdefault(
                text_id,
                {
                    "text_id": text_id,
                    "text": evidence["text"],
                    "confidence": evidence.get("confidence", "unknown"),
                    "event_ids": [],
                    "occurrences": [],
                },
            )
            if event["event_id"] not in entry["event_ids"]:
                entry["event_ids"].append(event["event_id"])
            entry["occurrences"].append(
                {
                    "event_id": event["event_id"],
                    "event_label": event["event_label"],
                    "line": event["line"],
                    "source_subscript": evidence["source_subscript"],
                }
            )

    texts = sorted(texts_by_id.values(), key=lambda item: (-len(item["event_ids"]), item["text_id"]))
    for entry in texts:
        entry["occurrences"] = sorted(entry["occurrences"], key=lambda item: (item["line"], item["event_id"], item["source_subscript"]))
        entry["event_count"] = len(entry["event_ids"])

    text_event_counts = {entry["text_id"]: len(entry["event_ids"]) for entry in texts}

    def rank_event_texts(event: dict) -> list[int]:
        ids = [e["text_id"] for e in event.get("evidence", [])]
        seen: set[int] = set()
        unique_ids: list[int] = []
        for text_id in ids:
            if text_id in seen:
                continue
            seen.add(text_id)
            unique_ids.append(text_id)
        return sorted(unique_ids, key=lambda text_id: (text_event_counts.get(text_id, 0), text_id))

    def build_line_signatures(events: list[dict]) -> list[dict]:
        seen_texts: set[int] = set()
        rows: list[dict] = []
        for event in events:
            ranked = rank_event_texts(event)
            signature = [text_id for text_id in ranked if text_id not in seen_texts]
            if not signature and ranked:
                signature = ranked[:2]
            seen_texts.update(signature)
            rows.append(
                {
                    "event_id": event["event_id"],
                    "event_label": event["event_label"],
                    "text_ids": [e["text_id"] for e in event.get("evidence", [])],
                    "ranked_text_ids": ranked,
                    "signature_text_ids": signature,
                }
            )
        return rows

    lines = {
        "schema": "sea2_event_text_index_v1",
        "source": {
            "bridge": str(BRIDGE.relative_to(ROOT)),
        },
        "summary": {
            "event_count": len(bridge["events"]),
            "text_count": len(texts),
            "shared_text_count": sum(1 for entry in texts if len(entry["event_ids"]) > 1),
        },
        "texts": texts,
        "events_by_line": {
            line: build_line_signatures(events)
            for line, events in sorted(events_by_line.items())
        },
    }
    return lines


def build_report(index: dict) -> str:
    lines = [
        "# Event Text Index",
        "",
        f"- schema: `{index['schema']}`",
        f"- bridge: `{index['source']['bridge']}`",
        f"- events: {index['summary']['event_count']}",
        f"- unique_texts: {index['summary']['text_count']}",
        f"- shared_texts: {index['summary']['shared_text_count']}",
        "",
        "## Shared Text Hotspots",
    ]
    shared = [entry for entry in index["texts"] if len(entry["event_ids"]) > 1]
    for entry in shared[:20]:
        snippet = entry["text"].replace("\n", " / ")
        lines.append(
            f"- text#{entry['text_id']} | events={len(entry['event_ids'])} | {snippet}"
        )
    lines.append("")
    lines.append("## By Line")
    for line, events in index["events_by_line"].items():
        lines.append(f"### {line}")
        for event in events:
            ranked_ids = ", ".join(f"#{text_id}" for text_id in event["ranked_text_ids"][:8])
            signature_ids = ", ".join(f"#{text_id}" for text_id in event["signature_text_ids"][:8])
            raw_ids = ", ".join(f"#{text_id}" for text_id in event["text_ids"][:8])
            lines.append(f"- {event['event_id']} {event['event_label']} | signature={signature_ids} | ranked={ranked_ids} | raw={raw_ids}")
    return "\n".join(lines) + "\n"


def main() -> None:
    index = build_index()
    json_path = OUT_DIR / "event_text_index_v1.json"
    md_path = OUT_DIR / "event_text_index_v1.md"
    json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(index), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
