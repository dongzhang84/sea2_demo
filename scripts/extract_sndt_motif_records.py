#!/usr/bin/env python3
"""Extract structured c0/cc/c8/c7 motif records from SNDT bytecode.

This promotes the repeated byte motif:

  c0 <selector> cc <u16> c8 <u16> c7

into records and contiguous runs. The names are intentionally neutral:
runtime validation has not proven the semantics yet.
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


def parse_code_areas(path: Path) -> list[tuple[str, int, bytes]]:
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
    areas: list[tuple[str, int, bytes]] = []
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
            areas.append((f"{snr}.chunk{ci}.sub{si}", pos, data[pos:sub_end]))
    return areas


def scan_records(script_id: str, code_start: int, code: bytes) -> list[dict]:
    records = []
    for pos in range(0, max(0, len(code) - 8)):
        if code[pos] != 0xC0 or code[pos + 2] != 0xCC or code[pos + 5] != 0xC8 or code[pos + 8] != 0xC7:
            continue
        records.append(
            {
                "script": script_id,
                "offset": pos,
                "offset_hex": f"0x{pos:04x}",
                "abs_offset": code_start + pos,
                "abs_offset_hex": f"0x{code_start + pos:04x}",
                "bytes": code[pos : pos + 9].hex(" "),
                "selector": code[pos + 1],
                "cc_arg": (code[pos + 3] << 8) | code[pos + 4],
                "c8_arg": (code[pos + 6] << 8) | code[pos + 7],
            }
        )
    return records


def build_runs(records: list[dict]) -> list[dict]:
    by_script: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_script[record["script"]].append(record)

    runs = []
    for script, script_records in by_script.items():
        sorted_records = sorted(script_records, key=lambda r: r["offset"])
        current: list[dict] = []
        for record in sorted_records:
            if not current or record["offset"] == current[-1]["offset"] + 9:
                current.append(record)
                continue
            runs.append(summarize_run(script, current))
            current = [record]
        if current:
            runs.append(summarize_run(script, current))
    return runs


def summarize_run(script: str, records: list[dict]) -> dict:
    c8_values = [r["c8_arg"] for r in records]
    cc_values = [r["cc_arg"] for r in records]
    selectors = [r["selector"] for r in records]
    return {
        "script": script,
        "start": records[0]["offset"],
        "start_hex": records[0]["offset_hex"],
        "end": records[-1]["offset"] + 9,
        "end_hex": f"0x{records[-1]['offset'] + 9:04x}",
        "count": len(records),
        "selectors": sorted(set(selectors)),
        "cc_args": sorted(set(cc_values)),
        "c8_min": min(c8_values),
        "c8_max": max(c8_values),
        "c8_monotonic_step1": all(b == a + 1 for a, b in zip(c8_values, c8_values[1:])),
        "records": records,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    for snr_id in range(7):
        for script_id, code_start, code in parse_code_areas(KOUKAI / f"Snr{snr_id}.dat"):
            records.extend(scan_records(script_id, code_start, code))

    runs = build_runs(records)
    by_script = Counter(r["script"] for r in records)
    selector_counts = Counter(r["selector"] for r in records)
    cc_counts = Counter(r["cc_arg"] for r in records)
    run_lengths = Counter(run["count"] for run in runs)

    result = {
        "record_count": len(records),
        "run_count": len(runs),
        "top_scripts": by_script.most_common(40),
        "selector_counts": selector_counts.most_common(),
        "cc_arg_counts": cc_counts.most_common(80),
        "run_length_counts": run_lengths.most_common(),
        "longest_runs": sorted(runs, key=lambda r: r["count"], reverse=True)[:80],
        "records": records,
        "runs": runs,
    }
    (OUT_DIR / "sndt_motif_records.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# SNDT Motif Records",
        "",
        f"- Records: `{len(records)}`",
        f"- Contiguous runs: `{len(runs)}`",
        "",
        "## Selector Counts",
        "",
    ]
    for selector, count in selector_counts.most_common():
        lines.append(f"- `{selector}`: {count}")
    lines += ["", "## Top Scripts", ""]
    for script, count in by_script.most_common(30):
        lines.append(f"- `{script}`: {count}")
    lines += ["", "## Longest Runs", ""]
    for run in sorted(runs, key=lambda r: r["count"], reverse=True)[:40]:
        lines.append(
            f"- `{run['script']}:{run['start_hex']}..{run['end_hex']}` "
            f"count={run['count']} selectors={run['selectors']} "
            f"cc={run['cc_args']} c8={run['c8_min']}..{run['c8_max']} "
            f"step1={run['c8_monotonic_step1']}"
        )
    (OUT_DIR / "sndt_motif_records.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_motif_records.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_motif_records.md'}")


if __name__ == "__main__":
    main()
