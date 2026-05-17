#!/usr/bin/env python3
"""Export a readable topology slice for João's opening script."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOPOLOGY = ROOT / "output" / "sndt_topology" / "topology_v0_motif.json"
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

    return {
        "schema": "joao_opening_topology_slice_v1",
        "source_script": SCRIPT_ID,
        "warning": "Static dialogue topology slice: scene order follows bytecode order, not yet proven runtime order.",
        "summary": {
            "scene_count": len(scenes),
            "record_count": sum(scene["record_count"] for scene in scenes),
            "text_range": [min(scene["text_range"][0] for scene in scenes), max(scene["text_range"][1] for scene in scenes)],
        },
        "scenes": scenes,
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
        f"- Text range: `{data['summary']['text_range'][0]}..{data['summary']['text_range'][1]}`",
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
    for index, scene in enumerate(data["scenes"]):
        node = f"scene_{index:02d}"
        speakers = ", ".join(scene["speakers"][:3]) or "-"
        first_text = scene["records"][0]["text"].replace("\\", "\\\\").replace('"', '\\"')
        label = (
            f"{scene['id']}\\n"
            f"text {scene['text_range'][0]}..{scene['text_range'][1]}\\n"
            f"speakers {speakers}\\n"
            f"{first_text}"
        )
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
