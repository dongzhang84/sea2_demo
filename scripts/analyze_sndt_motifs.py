#!/usr/bin/env python3
"""Analyze repeated bytecode motifs in SNDT scripts.

This is a static helper for recovering opcode lengths. It does not claim to
decode control flow; it looks for repeated local byte patterns that strongly
suggest fixed instruction widths.

The first target is the common motif visible in Snr4:

  c0 ?? cc ?? ?? c8 ?? ?? c7

If this motif is systematic, it supports candidate lengths:

  c0 len=2
  cc len=3
  c8 len=3
  c7 len=1
"""
from __future__ import annotations

import json
import struct
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_analysis"


def u16be(data: bytes, off: int) -> int:
    return struct.unpack_from(">H", data, off)[0]


def u32be(data: bytes, off: int) -> int:
    return struct.unpack_from(">I", data, off)[0]


def parse_code_areas(path: Path) -> list[tuple[str, bytes]]:
    data = path.read_bytes()
    offsets: list[int] = []
    pos = 0x10
    while True:
        value = u32be(data, pos)
        pos += 4
        if value == 0xFFFFFFFF:
            break
        offsets.append(value)
    bounds = offsets + [len(data)]

    areas: list[tuple[str, bytes]] = []
    snr = path.stem
    for ci, (start, end) in enumerate(zip(bounds, bounds[1:])):
        subs: list[int] = []
        pos = start
        while pos + 2 <= end:
            value = u16be(data, pos)
            pos += 2
            if value == 0xFFFF:
                break
            subs.append(value)
        sub_abs = [start + rel for rel in subs] + [end]
        for si in range(len(subs)):
            sub_start = sub_abs[si]
            sub_end = sub_abs[si + 1]
            pos = sub_start
            while pos + 2 <= sub_end:
                key = u16be(data, pos)
                if key == 0xFFFF:
                    pos += 2
                    if pos + 2 <= sub_end and u16be(data, pos) == 0xFFFF:
                        pos += 2
                    break
                pos += 4
            areas.append((f"{snr}.chunk{ci}.sub{si}", data[pos:sub_end]))
    return areas


def scan_structured_motifs(areas: list[tuple[str, bytes]]) -> list[dict]:
    hits: list[dict] = []
    for name, code in areas:
        for i in range(0, max(0, len(code) - 8)):
            if code[i] == 0xC0 and code[i + 2] == 0xCC and code[i + 5] == 0xC8 and code[i + 8] == 0xC7:
                hits.append(
                    {
                        "script": name,
                        "offset": i,
                        "offset_hex": f"0x{i:04x}",
                        "bytes": code[i : i + 9].hex(" "),
                        "c0_arg": code[i + 1],
                        "cc_arg": (code[i + 3] << 8) | code[i + 4],
                        "c8_arg": (code[i + 6] << 8) | code[i + 7],
                    }
                )
    return hits


def ngrams(areas: list[tuple[str, bytes]], n: int, limit: int = 50) -> list[dict]:
    counts: Counter[bytes] = Counter()
    examples: dict[bytes, str] = {}
    for name, code in areas:
        for i in range(0, max(0, len(code) - n + 1)):
            gram = code[i : i + n]
            counts[gram] += 1
            examples.setdefault(gram, f"{name}@0x{i:04x}")
    return [
        {"bytes": gram.hex(" "), "count": count, "example": examples[gram]}
        for gram, count in counts.most_common(limit)
    ]


def opcode_contexts(areas: list[tuple[str, bytes]], opcodes: list[int]) -> dict[str, list[dict]]:
    contexts: dict[str, list[dict]] = defaultdict(list)
    for name, code in areas:
        for i, value in enumerate(code):
            if value not in opcodes:
                continue
            key = f"0x{value:02x}"
            if len(contexts[key]) >= 80:
                continue
            lo = max(0, i - 4)
            hi = min(len(code), i + 10)
            contexts[key].append(
                {
                    "script": name,
                    "offset": i,
                    "offset_hex": f"0x{i:04x}",
                    "context": code[lo:hi].hex(" "),
                }
            )
    return dict(contexts)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    areas: list[tuple[str, bytes]] = []
    for snr_id in range(7):
        areas.extend(parse_code_areas(KOUKAI / f"Snr{snr_id}.dat"))

    motif_hits = scan_structured_motifs(areas)
    result = {
        "code_areas": len(areas),
        "total_code_bytes": sum(len(code) for _, code in areas),
        "c0_cc_c8_c7_hits": len(motif_hits),
        "c0_cc_c8_c7_examples": motif_hits[:200],
        "top_3grams": ngrams(areas, 3),
        "top_4grams": ngrams(areas, 4),
        "top_5grams": ngrams(areas, 5),
        "opcode_contexts": opcode_contexts(areas, [0x0C, 0xC0, 0xC7, 0xC8, 0xCC, 0xAD, 0xAC, 0xFE]),
    }

    (OUT_DIR / "sndt_motifs.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# SNDT Motif Analysis",
        "",
        f"- Code areas: `{result['code_areas']}`",
        f"- Total code bytes: `{result['total_code_bytes']}`",
        f"- `c0 ?? cc ???? c8 ???? c7` hits: `{result['c0_cc_c8_c7_hits']}`",
        "",
        "## Candidate Length Signal",
        "",
        "The structured motif supports this candidate split:",
        "",
        "```text",
        "c0 ??        -> candidate len 2",
        "cc ?? ??     -> candidate len 3",
        "c8 ?? ??     -> candidate len 3",
        "c7           -> candidate len 1",
        "```",
        "",
        "## First Motif Examples",
        "",
    ]
    for hit in motif_hits[:40]:
        lines.append(f"- `{hit['script']}:{hit['offset_hex']}` `{hit['bytes']}`")
    (OUT_DIR / "sndt_motifs.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_motifs.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_motifs.md'}")


if __name__ == "__main__":
    main()
