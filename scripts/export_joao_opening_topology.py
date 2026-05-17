#!/usr/bin/env python3
"""Export a readable topology slice for João's opening script."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOPOLOGY = ROOT / "output" / "sndt_topology" / "topology_v0_motif.json"
SHORT_MOTIFS = ROOT / "output" / "sndt_analysis" / "sndt_short_text_motifs.json"
OUT_DIR = ROOT / "output" / "sndt_topology"
SCRIPT_ID = "Snr1.chunk0.sub0"


def scene_title(run: dict) -> str:
    speakers = [speaker for speaker in run["speakers"] if speaker]
    if speakers:
        return " / ".join(speakers[:3])
    if run["cc_args"] == [0]:
        return "João self/default lines"
    return "Unresolved dialogue segment"


def build_slice(topology: dict) -> dict:
    target = None
    for file_info in topology["files"]:
        for chunk in file_info["chunks"]:
            for sub in chunk["subscripts"]:
                if sub["id"] == SCRIPT_ID:
                    target = sub
                    break
            if target:
                break
        if target:
            break
    if not target:
        raise ValueError(f"missing {SCRIPT_ID}")

    scenes = []
    for run in target["motif_runs"]:
        speaker_counts = Counter(record.get("resolved_speaker") or "" for record in run["records"])
        speakers = [speaker for speaker, _ in speaker_counts.most_common() if speaker]
        selectors = Counter(record["selector"] for record in run["records"])
        cc_counts = Counter(record["cc_arg"] for record in run["records"])
        records = [
            {
                "offset_hex": record["offset_hex"],
                "selector": record["selector"],
                "cc_arg": record["cc_arg"],
                "speaker": record.get("resolved_speaker"),
                "text_id": record["text_id"],
                "text": record["text_preview"],
            }
            for record in run["records"]
        ]
        scenes.append(
            {
                "id": run["id"],
                "title": "",
                "start": run["start"],
                "start_hex": f"0x{run['start']:04x}",
                "end": run["end"],
                "end_hex": f"0x{run['end']:04x}",
                "record_count": run["count"],
                "text_range": [run["c8_min"], run["c8_max"]],
                "selectors": dict(selectors.most_common()),
                "cc_args": [cc for cc, _ in cc_counts.most_common()],
                "speakers": speakers,
                "records": records,
            }
        )
        scenes[-1]["title"] = scene_title(scenes[-1])

    short_records = []
    if SHORT_MOTIFS.exists():
        short_data = json.loads(SHORT_MOTIFS.read_text())
        short_records = [
            {
                "id": f"{SCRIPT_ID}.short{index}",
                "kind": "short_text",
                "start": record["offset"],
                "start_hex": record["offset_hex"],
                "end": record["offset"] + 6,
                "end_hex": f"0x{record['offset'] + 6:04x}",
                "text_id": record["text_id"],
                "text": record["text_preview"],
            }
            for index, record in enumerate(short_data["records"])
            if record["script"] == SCRIPT_ID
        ]

    timeline = []
    for scene in scenes:
        timeline.append(
            {
                "kind": "motif_scene",
                "id": scene["id"],
                "start": scene["start"],
                "start_hex": scene["start_hex"],
                "end": scene["end"],
                "end_hex": scene["end_hex"],
                "text_range": scene["text_range"],
                "record_count": scene["record_count"],
                "speakers": scene["speakers"],
                "title": scene["title"],
            }
        )
    timeline.extend(short_records)
    timeline.sort(key=lambda item: (item["start"], 0 if item["kind"] == "motif_scene" else 1))

    all_text_ids = {record["text_id"] for scene in scenes for record in scene["records"]}
    all_text_ids.update(record["text_id"] for record in short_records)

    return {
        "schema": "joao_opening_topology_slice_v1",
        "source_script": SCRIPT_ID,
        "warning": "Static dialogue topology slice: timeline follows bytecode order, not yet proven runtime order.",
        "summary": {
            "scene_count": len(scenes),
            "record_count": sum(scene["record_count"] for scene in scenes),
            "short_text_count": len(short_records),
            "timeline_items": len(timeline),
            "text_range": [min(all_text_ids), max(all_text_ids)],
            "text_coverage_count": len(all_text_ids),
            "missing_text_ids_in_range": [
                text_id for text_id in range(min(all_text_ids), max(all_text_ids) + 1) if text_id not in all_text_ids
            ],
        },
        "scenes": scenes,
        "short_text_records": short_records,
        "timeline": timeline,
    }


def write_markdown(data: dict) -> None:
    lines = [
        "# João Opening Topology Slice",
        "",
        "This is a static, readable topology slice for `Snr1.chunk0.sub0`.",
        "It groups the `c0/cc/c8/c7` motif records into contiguous dialogue/event segments.",
        "",
        f"- Scenes/runs: `{data['summary']['scene_count']}`",
        f"- Records: `{data['summary']['record_count']}`",
        f"- Short text records: `{data['summary']['short_text_count']}`",
        f"- Timeline items: `{data['summary']['timeline_items']}`",
        f"- Text range: `{data['summary']['text_range'][0]}..{data['summary']['text_range'][1]}`",
        f"- Text coverage count: `{data['summary']['text_coverage_count']}`",
        f"- Missing text IDs in range: `{data['summary']['missing_text_ids_in_range']}`",
        "",
        "## Bytecode Timeline",
        "",
        "| Item | Kind | Offset | Text | Speakers / Preview |",
        "|---|---|---|---|---|",
    ]
    for item in data["timeline"]:
        if item["kind"] == "motif_scene":
            speakers = ", ".join(item["speakers"]) or "-"
            text = f"{item['text_range'][0]}..{item['text_range'][1]}"
            preview = f"{item['title']} / {speakers}"
        else:
            text = str(item["text_id"])
            preview = item["text"]
        lines.append(
            f"| `{item['id']}` | {item['kind']} | `{item['start_hex']}..{item['end_hex']}` | {text} | {preview} |"
        )

    lines += [
        "",
        "## Scene Index",
        "",
        "| Scene | Offset | Text IDs | Records | Speakers |",
        "|---|---|---|---:|---|",
    ]
    for scene in data["scenes"]:
        speakers = ", ".join(scene["speakers"]) or "-"
        lines.append(
            f"| `{scene['id']}` | `{scene['start_hex']}..{scene['end_hex']}` | "
            f"{scene['text_range'][0]}..{scene['text_range'][1]} | {scene['record_count']} | {speakers} |"
        )

    lines += ["", "## Dialogue Segments", ""]
    for scene in data["scenes"]:
        speakers = ", ".join(scene["speakers"]) or "-"
        lines += [
            f"### {scene['id']} - {scene['title']}",
            "",
            f"- Offset: `{scene['start_hex']}..{scene['end_hex']}`",
            f"- Text IDs: `{scene['text_range'][0]}..{scene['text_range'][1]}`",
            f"- Selectors: `{scene['selectors']}`",
            f"- cc_args: `{scene['cc_args']}`",
            f"- Speakers: `{speakers}`",
            "",
        ]
        for record in scene["records"]:
            speaker = record["speaker"] or "-"
            lines.append(
                f"- sel={record['selector']} cc={record['cc_arg']} speaker={speaker} "
                f"text={record['text_id']}: {record['text']}"
            )
        lines.append("")

    (OUT_DIR / "joao_opening_topology.md").write_text("\n".join(lines) + "\n")


def write_dot(data: dict) -> None:
    lines = [
        "digraph joao_opening_topology {",
        "  graph [rankdir=LR];",
        "  node [shape=box, fontname=\"Menlo\"];",
    ]
    previous = None
    for index, item in enumerate(data["timeline"]):
        node = f"item_{index:03d}"
        if item["kind"] == "motif_scene":
            speakers = ", ".join(item["speakers"][:3]) or "-"
            label = (
                f"{item['id']}\\n"
                f"text {item['text_range'][0]}..{item['text_range'][1]}\\n"
                f"speakers {speakers}\\n"
                f"{item['title']}"
            )
        else:
            preview = item["text"].replace("\\", "\\\\").replace('"', '\\"')
            label = f"{item['id']}\\nshort text {item['text_id']}\\n{preview}"
        lines.append(f"  {node} [label=\"{label}\"];")
        if previous:
            lines.append(f"  {previous} -> {node} [label=\"bytecode next\"];")
        previous = node
    lines.append("}")
    (OUT_DIR / "joao_opening_topology.dot").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    topology = json.loads(TOPOLOGY.read_text())
    data = build_slice(topology)
    (OUT_DIR / "joao_opening_topology.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    write_markdown(data)
    write_dot(data)
    print(f"Wrote {OUT_DIR / 'joao_opening_topology.json'}")
    print(f"Wrote {OUT_DIR / 'joao_opening_topology.md'}")
    print(f"Wrote {OUT_DIR / 'joao_opening_topology.dot'}")


if __name__ == "__main__":
    main()
