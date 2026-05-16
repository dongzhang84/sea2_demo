#!/usr/bin/env python3
"""Export a conservative SNDT topology snapshot.

This does not claim to decompile the SNDT VM. It exports the parts that are
already structurally known:

- SNDT file/chunk/subscript boundaries
- dispatch-table edges at the beginning of each subscript
- raw 0x0c text references, marked as noisy until opcode lengths are known

Outputs:
  output/sndt_topology/sndt_topology.json
  output/sndt_topology/sndt_topology.dot
  output/sndt_topology/sndt_text_refs.md
"""
from __future__ import annotations

import json
import struct
from dataclasses import dataclass
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from decode_text import decode_file  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_topology"


@dataclass
class Chunk:
    index: int
    start: int
    end: int
    subs: list[int]


def read_u16be(data: bytes, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def read_u32be(data: bytes, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]


def parse_sndt(path: Path) -> tuple[bytes, list[Chunk]]:
    data = path.read_bytes()
    if data[:4] != b"SNDT":
        raise ValueError(f"{path} is not an SNDT file")

    chunk_offsets: list[int] = []
    pos = 0x10
    while pos + 4 <= len(data):
        value = read_u32be(data, pos)
        pos += 4
        if value == 0xFFFFFFFF:
            break
        chunk_offsets.append(value)

    bounds = chunk_offsets + [len(data)]
    chunks: list[Chunk] = []
    for index, (start, end) in enumerate(zip(bounds, bounds[1:])):
        subs: list[int] = []
        pos = start
        while pos + 2 <= end:
            value = read_u16be(data, pos)
            pos += 2
            if value == 0xFFFF:
                break
            subs.append(value)
        chunks.append(Chunk(index=index, start=start, end=end, subs=subs))
    return data, chunks


def parse_dispatch_table(data: bytes, start: int, end: int) -> tuple[list[dict], int]:
    entries: list[dict] = []
    pos = start
    while pos + 2 <= end:
        key = read_u16be(data, pos)
        if key == 0xFFFF:
            pos += 2
            if pos + 2 <= end and read_u16be(data, pos) == 0xFFFF:
                pos += 2
            return entries, pos
        if pos + 4 > end:
            break
        target = read_u16be(data, pos + 2)
        entries.append(
            {
                "key": key,
                "key_hex": f"0x{key:04x}",
                "tag": key >> 8,
                "selector": key & 0xFF,
                "target_rel": target,
                "target_hex": f"0x{target:04x}",
            }
        )
        pos += 4
    return entries, pos


def scan_text_refs(code: bytes, mes: list[str]) -> list[dict]:
    refs: list[dict] = []
    for pos in range(max(0, len(code) - 1)):
        if code[pos] != 0x0C:
            continue
        text_id = code[pos + 1]
        if text_id >= len(mes):
            continue
        text = mes[text_id].replace("\n", "\\n")
        refs.append(
            {
                "offset_rel": pos,
                "offset_hex": f"0x{pos:04x}",
                "text_id": text_id,
                "confidence": "noisy",
                "text": text,
            }
        )
    return refs


def build_topology() -> dict:
    files = []
    for snr_id in range(7):
        dat_path = KOUKAI / f"Snr{snr_id}.dat"
        mes_path = KOUKAI / f"Snr{snr_id}.mes"
        data, chunks = parse_sndt(dat_path)
        mes = decode_file(str(mes_path))

        file_info = {
            "id": f"Snr{snr_id}",
            "dat_path": str(dat_path),
            "mes_path": str(mes_path),
            "size": len(data),
            "text_count": len(mes),
            "chunks": [],
        }

        for chunk in chunks:
            sub_abs = [chunk.start + rel for rel in chunk.subs] + [chunk.end]
            chunk_info = {
                "id": f"Snr{snr_id}.chunk{chunk.index}",
                "index": chunk.index,
                "start": chunk.start,
                "end": chunk.end,
                "size": chunk.end - chunk.start,
                "subscripts": [],
            }

            for sub_index, rel_start in enumerate(chunk.subs):
                start = sub_abs[sub_index]
                end = sub_abs[sub_index + 1]
                dispatch, code_start = parse_dispatch_table(data, start, end)
                code = data[code_start:end]
                sub_id = f"Snr{snr_id}.chunk{chunk.index}.sub{sub_index}"
                chunk_info["subscripts"].append(
                    {
                        "id": sub_id,
                        "index": sub_index,
                        "start": start,
                        "start_hex": f"0x{start:04x}",
                        "end": end,
                        "end_hex": f"0x{end:04x}",
                        "size": end - start,
                        "code_start": code_start,
                        "code_start_hex": f"0x{code_start:04x}",
                        "dispatch": dispatch,
                        "text_refs": scan_text_refs(code, mes),
                    }
                )
            file_info["chunks"].append(chunk_info)
        files.append(file_info)
    return {
        "schema": "sndt_topology_static_v1",
        "source_dir": str(KOUKAI),
        "warning": (
            "Text references are noisy until SNDT opcode lengths are recovered. "
            "Dispatch tables and container boundaries are structural facts."
        ),
        "files": files,
    }


def write_json(topology: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "sndt_topology.json"
    path.write_text(json.dumps(topology, ensure_ascii=False, indent=2) + "\n")


def write_dot(topology: dict) -> None:
    lines = [
        "digraph sndt_topology {",
        "  graph [rankdir=LR];",
        "  node [shape=box, fontname=\"Menlo\"];",
    ]
    for file_info in topology["files"]:
        for chunk in file_info["chunks"]:
            for sub in chunk["subscripts"]:
                node_id = sub["id"].replace(".", "_")
                label = f"{sub['id']}\\ncode {sub['code_start_hex']}\\ntexts {len(sub['text_refs'])}"
                lines.append(f"  {node_id} [label=\"{label}\"];")
                for edge in sub["dispatch"]:
                    target_node = f"{chunk['id']}.off_{edge['target_hex']}".replace(".", "_")
                    target_label = f"{chunk['id']}\\n{edge['target_hex']}"
                    lines.append(f"  {target_node} [label=\"{target_label}\", shape=ellipse];")
                    edge_label = f"tag {edge['tag']:02x} sel {edge['selector']:02x}"
                    lines.append(f"  {node_id} -> {target_node} [label=\"{edge_label}\"];")
    lines.append("}")
    (OUT_DIR / "sndt_topology.dot").write_text("\n".join(lines) + "\n")


def write_text_refs(topology: dict) -> None:
    lines = [
        "# SNDT Text References",
        "",
        "These references are raw `0x0c XX` scans inside each subscript code area.",
        "They are useful for orientation, but remain noisy until opcode lengths are known.",
        "",
    ]
    for file_info in topology["files"]:
        lines.append(f"## {file_info['id']}")
        lines.append("")
        for chunk in file_info["chunks"]:
            lines.append(f"### {chunk['id']}")
            lines.append("")
            for sub in chunk["subscripts"]:
                refs = sub["text_refs"]
                if not refs:
                    continue
                lines.append(f"#### {sub['id']}")
                lines.append("")
                for ref in refs[:40]:
                    text = ref["text"]
                    if len(text) > 100:
                        text = text[:97] + "..."
                    lines.append(
                        f"- `{ref['offset_hex']}` text[{ref['text_id']}], "
                        f"{ref['confidence']}: {text}"
                    )
                if len(refs) > 40:
                    lines.append(f"- ... {len(refs) - 40} more refs omitted")
                lines.append("")
    (OUT_DIR / "sndt_text_refs.md").write_text("\n".join(lines))


def main() -> None:
    topology = build_topology()
    write_json(topology)
    write_dot(topology)
    write_text_refs(topology)
    print(f"Wrote {OUT_DIR / 'sndt_topology.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_topology.dot'}")
    print(f"Wrote {OUT_DIR / 'sndt_text_refs.md'}")


if __name__ == "__main__":
    main()
