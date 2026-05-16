#!/usr/bin/env python3
"""Export topology v0 with motif-run nodes.

This combines the existing SNDT container topology with c0/cc/c8/c7 motif runs.
It is not a full execution graph yet; it is an intermediate graph where
subscripts contain structured internal table nodes.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
STATIC_TOPOLOGY = ROOT / "output" / "sndt_topology" / "sndt_topology.json"
MOTIF_RECORDS = ROOT / "output" / "sndt_analysis" / "sndt_motif_records.json"
OUT_DIR = ROOT / "output" / "sndt_topology"


def load_inputs() -> tuple[dict, dict]:
    return json.loads(STATIC_TOPOLOGY.read_text()), json.loads(MOTIF_RECORDS.read_text())


def build_motif_index(motif_data: dict) -> dict[str, list[dict]]:
    by_script: dict[str, list[dict]] = {}
    for run in motif_data["runs"]:
        by_script.setdefault(run["script"], []).append(run)
    for runs in by_script.values():
        runs.sort(key=lambda r: r["start"])
    return by_script


def build_topology(static: dict, motif_data: dict) -> dict:
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
                        f"c8 {run['c8_min']}..{run['c8_max']}"
                    )
                    lines.append(f"  {run_node} [shape=ellipse, label=\"{run_label}\"];")
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
