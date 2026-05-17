#!/usr/bin/env python3
"""Extract short SNDT text motif records of the form c0 00 c8 <u16> c7."""
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
OUT_DIR = ROOT / "output" / "sndt_analysis"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402
from extract_sndt_motif_records import parse_code_areas  # noqa: E402


SNR_RE = re.compile(r"Snr(\d+)\.")


def snr_id_for_script(script: str) -> int:
    match = SNR_RE.match(script)
    if not match:
        raise ValueError(script)
    return int(match.group(1))


def preview(text: str, limit: int = 96) -> str:
    text = text.replace("\n", "\\n")
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def scan_short_records(script_id: str, code_start: int, code: bytes, texts: list[str]) -> list[dict]:
    records = []
    for pos in range(0, max(0, len(code) - 5)):
        if code[pos : pos + 3] != b"\xc0\x00\xc8" or code[pos + 5] != 0xC7:
            continue
        text_id = (code[pos + 3] << 8) | code[pos + 4]
        if text_id >= len(texts):
            continue
        records.append(
            {
                "script": script_id,
                "offset": pos,
                "offset_hex": f"0x{pos:04x}",
                "abs_offset": code_start + pos,
                "abs_offset_hex": f"0x{code_start + pos:04x}",
                "bytes": code[pos : pos + 6].hex(" "),
                "text_id": text_id,
                "text_preview": preview(texts[text_id]),
            }
        )
    return records


def build_runs(records: list[dict]) -> list[dict]:
    by_script: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_script[record["script"]].append(record)
    runs = []
    for script, script_records in by_script.items():
        current = []
        for record in sorted(script_records, key=lambda item: item["offset"]):
            if not current or record["offset"] == current[-1]["offset"] + 6:
                current.append(record)
            else:
                runs.append(summarize_run(script, current))
                current = [record]
        if current:
            runs.append(summarize_run(script, current))
    return runs


def summarize_run(script: str, records: list[dict]) -> dict:
    text_ids = [record["text_id"] for record in records]
    return {
        "script": script,
        "start": records[0]["offset"],
        "start_hex": records[0]["offset_hex"],
        "end": records[-1]["offset"] + 6,
        "end_hex": f"0x{records[-1]['offset'] + 6:04x}",
        "count": len(records),
        "text_min": min(text_ids),
        "text_max": max(text_ids),
        "text_monotonic_step1": all(b == a + 1 for a, b in zip(text_ids, text_ids[1:])),
        "records": records,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for snr_id in range(7):
        texts = decode_file(str(KOUKAI / f"Snr{snr_id}.mes"))
        for script_id, code_start, code in parse_code_areas(KOUKAI / f"Snr{snr_id}.dat"):
            records.extend(scan_short_records(script_id, code_start, code, texts))
    runs = build_runs(records)
    by_script = Counter(record["script"] for record in records)
    result = {
        "schema": "sndt_short_text_motif_v1",
        "record_count": len(records),
        "run_count": len(runs),
        "top_scripts": by_script.most_common(40),
        "longest_runs": sorted(runs, key=lambda run: run["count"], reverse=True)[:80],
        "records": records,
        "runs": runs,
    }
    (OUT_DIR / "sndt_short_text_motifs.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    joao_records = [record for record in records if record["script"] == "Snr1.chunk0.sub0"]
    lines = [
        "# SNDT Short Text Motifs",
        "",
        "Extracts records shaped as `c0 00 c8 <text_id:u16> c7`.",
        "This appears in gaps between the longer `c0/cc/c8/c7` motif runs.",
        "",
        f"- Records: `{len(records)}`",
        f"- Runs: `{len(runs)}`",
        "",
        "## Top Scripts",
        "",
    ]
    for script, count in by_script.most_common(30):
        lines.append(f"- `{script}`: {count}")
    lines += ["", "## João Opening Records", ""]
    for record in joao_records:
        lines.append(
            f"- `{record['offset_hex']}` text={record['text_id']}: {record['text_preview']}"
        )
    (OUT_DIR / "sndt_short_text_motifs.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_short_text_motifs.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_short_text_motifs.md'}")


if __name__ == "__main__":
    main()
