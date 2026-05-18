#!/usr/bin/env python3
"""Export a readable script index from the static SNDT topology."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "sndt_topology"
TOPOLOGY = OUT_DIR / "sndt_topology.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def count_text_refs(subscript: dict) -> int:
    return len(subscript.get("text_refs", []))


def count_dispatch(subscript: dict) -> int:
    return len(subscript.get("dispatch", []))


def build_index() -> dict:
    topology = load_json(TOPOLOGY)
    files_out = []
    all_subscripts = []

    for file_info in topology["files"]:
        chunks_out = []
        file_text_refs = 0
        file_dispatch = 0
        file_subscripts = 0
        for chunk in file_info["chunks"]:
            subs = chunk["subscripts"]
            subscript_rows = []
            chunk_text_refs = 0
            chunk_dispatch = 0
            for sub in subs:
                ref_count = count_text_refs(sub)
                disp_count = count_dispatch(sub)
                row = {
                    "id": sub["id"],
                    "index": sub["index"],
                    "start": sub["start"],
                    "end": sub["end"],
                    "size": sub["size"],
                    "code_start": sub["code_start"],
                    "dispatch_count": disp_count,
                    "text_ref_count": ref_count,
                    "first_text_refs": sub.get("text_refs", [])[:5],
                }
                subscript_rows.append(row)
                all_subscripts.append(
                    {
                        "file": file_info["id"],
                        "chunk": chunk["id"],
                        **row,
                    }
                )
                chunk_text_refs += ref_count
                chunk_dispatch += disp_count
            chunks_out.append(
                {
                    "id": chunk["id"],
                    "index": chunk["index"],
                    "start": chunk["start"],
                    "end": chunk["end"],
                    "size": chunk["size"],
                    "subscript_count": len(subs),
                    "dispatch_count": chunk_dispatch,
                    "text_ref_count": chunk_text_refs,
                    "subscripts": subscript_rows,
                }
            )
            file_text_refs += chunk_text_refs
            file_dispatch += chunk_dispatch
            file_subscripts += len(subs)
        files_out.append(
            {
                "id": file_info["id"],
                "mes_path": file_info["mes_path"],
                "dat_path": file_info["dat_path"],
                "size": file_info["size"],
                "text_count": file_info["text_count"],
                "chunk_count": len(file_info["chunks"]),
                "subscript_count": file_subscripts,
                "dispatch_count": file_dispatch,
                "text_ref_count": file_text_refs,
                "chunks": chunks_out,
            }
        )

    all_subscripts.sort(key=lambda row: (-row["text_ref_count"], -row["dispatch_count"], row["id"]))
    return {
        "schema": "sea2_sndt_script_index_v1",
        "source": str(TOPOLOGY.relative_to(ROOT)),
        "files": files_out,
        "hotspots": {
            "subscripts_by_text_refs": all_subscripts[:80],
        },
    }


def build_report(index: dict) -> str:
    lines = [
        "# SNDT Script Index Report",
        "",
        f"- schema: `{index['schema']}`",
        f"- source: `{index['source']}`",
        f"- files: {len(index['files'])}",
        "",
        "## File Summary",
        "| File | Texts | Chunks | Subscripts | Dispatch | Text refs |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for file_info in index["files"]:
        lines.append(
            f"| {file_info['id']} | {file_info['text_count']} | {file_info['chunk_count']} | "
            f"{file_info['subscript_count']} | {file_info['dispatch_count']} | {file_info['text_ref_count']} |"
        )
    lines.extend(["", "## Hotspot Subscripts", "| Subscript | File | Chunk | Text refs | Dispatch |", "|---|---|---|---:|---:|"])
    for row in index["hotspots"]["subscripts_by_text_refs"][:40]:
        lines.append(
            f"| {row['id']} | {row['file']} | {row['chunk']} | {row['text_ref_count']} | {row['dispatch_count']} |"
        )
    lines.extend(["", "## File Details"])
    for file_info in index["files"]:
        lines.append(f"### {file_info['id']}")
        lines.append(
            f"- texts: {file_info['text_count']}, chunks: {file_info['chunk_count']}, subscripts: {file_info['subscript_count']}, "
            f"dispatch: {file_info['dispatch_count']}, text refs: {file_info['text_ref_count']}"
        )
        top_chunks = sorted(file_info["chunks"], key=lambda c: (-c["text_ref_count"], -c["dispatch_count"], c["id"]))[:5]
        for chunk in top_chunks:
            lines.append(
                f"- {chunk['id']}: subs={chunk['subscript_count']} dispatch={chunk['dispatch_count']} text_refs={chunk['text_ref_count']}"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    index = build_index()
    json_path = OUT_DIR / "sndt_script_index_v1.json"
    md_path = OUT_DIR / "sndt_script_index_v1.md"
    json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(build_report(index), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
