#!/usr/bin/env python3
"""Export topology v0 with motif-run nodes.

This combines the existing SNDT container topology with c0/cc/c8/c7 motif runs.
It is not a full execution graph yet; it is an intermediate graph where
subscripts contain structured internal table nodes.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
STATIC_TOPOLOGY = ROOT / "output" / "sndt_topology" / "sndt_topology.json"
MOTIF_RECORDS = ROOT / "output" / "sndt_analysis" / "sndt_motif_records.json"
OUT_DIR = ROOT / "output" / "sndt_topology"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402


SNR_RE = re.compile(r"Snr(\d+)\.")


def load_inputs() -> tuple[dict, dict]:
    return json.loads(STATIC_TOPOLOGY.read_text()), json.loads(MOTIF_RECORDS.read_text())


def load_texts() -> dict[int, list[str]]:
    return {snr_id: decode_file(str(KOUKAI / f"Snr{snr_id}.mes")) for snr_id in range(7)}


def snr_id_for_script(script: str) -> int:
    match = SNR_RE.match(script)
    if not match:
        raise ValueError(script)
    return int(match.group(1))


def text_preview(text: str, limit: int = 64) -> str:
    one_line = text.replace("\n", "\\n")
    if len(one_line) <= limit:
        return one_line
    return one_line[: limit - 3] + "..."


def motif_record_with_text(record: dict, texts: dict[int, list[str]]) -> dict:
    snr_id = snr_id_for_script(record["script"])
    text_id = record["c8_arg"]
    text = texts[snr_id][text_id] if 0 <= text_id < len(texts[snr_id]) else ""
    return {
        "offset": record["offset"],
        "offset_hex": record["offset_hex"],
        "selector": record["selector"],
        "cc_arg": record["cc_arg"],
        "text_id": text_id,
        "text_preview": text_preview(text),
    }


def build_motif_index(motif_data: dict) -> dict[str, list[dict]]:
    by_script: dict[str, list[dict]] = {}
    for run in motif_data["runs"]:
        by_script.setdefault(run["script"], []).append(run)
    for runs in by_script.values():
        runs.sort(key=lambda r: r["start"])
    return by_script


def speaker_for_text(text: str) -> str | None:
    match = re.match(r"^〔([^〕]+)〕", text)
    if not match:
        return None
    return match.group(1)


def build_speaker_hints(motif_data: dict, texts: dict[int, list[str]]) -> dict[tuple[str, int], Counter[str]]:
    hints: dict[tuple[str, int], Counter[str]] = defaultdict(Counter)
    for record in motif_data["records"]:
        snr_id = snr_id_for_script(record["script"])
        text_id = record["c8_arg"]
        text = texts[snr_id][text_id] if 0 <= text_id < len(texts[snr_id]) else ""
        speaker = speaker_for_text(text)
        if speaker:
            hints[(record["script"], record["cc_arg"])][speaker] += 1
    return hints


def resolved_speaker_for_record(record: dict, text: str, hints: dict[tuple[str, int], Counter[str]]) -> str | None:
    speaker = speaker_for_text(text)
    if speaker:
        return speaker
    candidates = hints.get((record["script"], record["cc_arg"]))
    if candidates:
        return candidates.most_common(1)[0][0]
    return None


def build_topology(static: dict, motif_data: dict) -> dict:
    texts = load_texts()
    speaker_hints = build_speaker_hints(motif_data, texts)
    motif_index = build_motif_index(motif_data)
    files = []
    for file_info in static["files"]:
        out_file = {"id": file_info["id"], "chunks": []}
        for chunk in file_info["chunks"]:
            out_chunk = {"id": chunk["id"], "subscripts": []}
            for sub in chunk["subscripts"]:
                runs = motif_index.get(sub["id"], [])
                out_chunk["subscripts"].append(
                    {
                        "id": sub["id"],
                        "code_start": sub["code_start"],
                        "dispatch": sub["dispatch"],
                        "text_refs": sub["text_refs"],
                        "motif_runs": [
                            {
                                "id": f"{sub['id']}.run{i}",
                                "start": run["start"],
                                "end": run["end"],
                                "count": run["count"],
                                "selectors": run["selectors"],
                                "cc_args": run["cc_args"],
                                "c8_min": run["c8_min"],
                                "c8_max": run["c8_max"],
                                "text_ids": [record["c8_arg"] for record in run["records"]],
                                "first_text": motif_record_with_text(run["records"][0], texts)["text_preview"],
                                "first_speaker": resolved_speaker_for_record(
                                    run["records"][0],
                                    texts[snr_id_for_script(run["records"][0]["script"])][run["records"][0]["c8_arg"]],
                                    speaker_hints,
                                ),
                                "records": [
                                    {
                                        **motif_record_with_text(record, texts),
                                        "resolved_speaker": resolved_speaker_for_record(
                                            record,
                                            texts[snr_id_for_script(record["script"])][record["c8_arg"]],
                                            speaker_hints,
                                        ),
                                    }
                                    for record in run["records"]
                                ],
                                "c8_monotonic_step1": run["c8_monotonic_step1"],
                            }
                            for i, run in enumerate(runs)
                        ],
                    }
                )
            out_file["chunks"].append(out_chunk)
        files.append(out_file)
    return {
        "schema": "sndt_topology_v0_motif",
        "warning": "Intermediate topology: motif runs are static structural nodes, not proven runtime branches.",
        "summary": {
            "motif_records": motif_data["record_count"],
            "motif_runs": motif_data["run_count"],
        },
        "files": files,
    }


def write_dot(topology: dict) -> None:
    lines = [
        "digraph sndt_topology_v0_motif {",
        "  graph [rankdir=LR];",
        "  node [shape=box, fontname=\"Menlo\"];",
    ]
    for file_info in topology["files"]:
        for chunk in file_info["chunks"]:
            for sub in chunk["subscripts"]:
                sub_node = sub["id"].replace(".", "_")
                label = f"{sub['id']}\\ntexts {len(sub['text_refs'])}\\nruns {len(sub['motif_runs'])}"
                lines.append(f"  {sub_node} [label=\"{label}\"];")
                for run in sub["motif_runs"]:
                    run_node = run["id"].replace(".", "_")
                    run_label = (
                        f"run {run['start']:04x}-{run['end']:04x}\\n"
                        f"count {run['count']}\\n"
                        f"sel {run['selectors']}\\n"
                        f"cc {run['cc_args'][:5]}\\n"
                        f"text {run['c8_min']}..{run['c8_max']}\\n"
                        f"speaker {run['first_speaker'] or '-'}\\n"
                        f"{run['first_text']}"
                    )
                    escaped_label = run_label.replace("\\", "\\\\").replace('"', '\\"')
                    lines.append(f"  {run_node} [shape=ellipse, label=\"{escaped_label}\"];")
                    lines.append(f"  {sub_node} -> {run_node} [label=\"contains\"];")
    lines.append("}")
    (OUT_DIR / "topology_v0_motif.dot").write_text("\n".join(lines) + "\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    static, motif_data = load_inputs()
    topology = build_topology(static, motif_data)
    (OUT_DIR / "topology_v0_motif.json").write_text(json.dumps(topology, ensure_ascii=False, indent=2) + "\n")
    write_dot(topology)
    print(f"Wrote {OUT_DIR / 'topology_v0_motif.json'}")
    print(f"Wrote {OUT_DIR / 'topology_v0_motif.dot'}")


if __name__ == "__main__":
    main()
