#!/usr/bin/env python3
"""Test whether motif c8_arg maps to Snr*.mes text ids."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
KOUKAI = Path("/Users/dong/Projects/Koukai2")
if not KOUKAI.exists():
    KOUKAI = ROOT / "game_dos"
OUT_DIR = ROOT / "output" / "sndt_analysis"
MOTIF_RECORDS = OUT_DIR / "sndt_motif_records.json"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402


SNR_RE = re.compile(r"Snr(\d+)\.")


def snr_id_for_script(script: str) -> int:
    match = SNR_RE.match(script)
    if not match:
        raise ValueError(script)
    return int(match.group(1))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    motif = json.loads(MOTIF_RECORDS.read_text())
    texts = {snr_id: decode_file(str(KOUKAI / f"Snr{snr_id}.mes")) for snr_id in range(7)}

    mapped = []
    unmapped = []
    by_script: Counter[str] = Counter()
    valid_by_script: Counter[str] = Counter()
    by_snr: Counter[int] = Counter()
    valid_by_snr: Counter[int] = Counter()

    for record in motif["records"]:
        snr_id = snr_id_for_script(record["script"])
        by_script[record["script"]] += 1
        by_snr[snr_id] += 1
        c8 = record["c8_arg"]
        entry = {
            "script": record["script"],
            "offset_hex": record["offset_hex"],
            "selector": record["selector"],
            "cc_arg": record["cc_arg"],
            "c8_arg": c8,
        }
        if 0 <= c8 < len(texts[snr_id]):
            entry["text"] = texts[snr_id][c8]
            mapped.append(entry)
            valid_by_script[record["script"]] += 1
            valid_by_snr[snr_id] += 1
        else:
            unmapped.append(entry)

    summary = {
        "total_records": len(motif["records"]),
        "mapped_to_text": len(mapped),
        "unmapped": len(unmapped),
        "mapped_ratio": len(mapped) / len(motif["records"]) if motif["records"] else 0,
        "by_snr": [
            {
                "snr": snr_id,
                "records": by_snr[snr_id],
                "mapped": valid_by_snr[snr_id],
                "text_count": len(texts[snr_id]),
                "ratio": valid_by_snr[snr_id] / by_snr[snr_id] if by_snr[snr_id] else 0,
            }
            for snr_id in range(7)
        ],
        "top_scripts": [
            {
                "script": script,
                "records": count,
                "mapped": valid_by_script[script],
                "ratio": valid_by_script[script] / count if count else 0,
            }
            for script, count in by_script.most_common(40)
        ],
        "mapped_examples": mapped[:500],
        "unmapped_examples": unmapped[:200],
    }

    (OUT_DIR / "sndt_motif_text_map.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# SNDT Motif Text Map",
        "",
        "This checks whether `c8_arg` in `c0/cc/c8/c7` motif records maps to the matching `Snr*.mes` text id.",
        "",
        f"- Total motif records: `{summary['total_records']}`",
        f"- Mapped to valid text id: `{summary['mapped_to_text']}`",
        f"- Unmapped: `{summary['unmapped']}`",
        f"- Mapped ratio: `{summary['mapped_ratio']:.3f}`",
        "",
        "## By SNDT File",
        "",
        "| SNDT | records | mapped | text_count | ratio |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in summary["by_snr"]:
        lines.append(
            f"| Snr{row['snr']} | {row['records']} | {row['mapped']} | {row['text_count']} | {row['ratio']:.3f} |"
        )
    lines += ["", "## Top Scripts", ""]
    for row in summary["top_scripts"][:30]:
        lines.append(f"- `{row['script']}` records={row['records']} mapped={row['mapped']} ratio={row['ratio']:.3f}")
    lines += ["", "## João Opening Examples", ""]
    for entry in mapped:
        if entry["script"] != "Snr1.chunk0.sub0":
            continue
        text = entry["text"].replace("\n", "\\n")
        if len(text) > 100:
            text = text[:97] + "..."
        lines.append(
            f"- `{entry['offset_hex']}` sel={entry['selector']} cc={entry['cc_arg']} "
            f"c8/text={entry['c8_arg']}: {text}"
        )
        if len([line for line in lines if line.startswith("- `0x")]) >= 80:
            break
    (OUT_DIR / "sndt_motif_text_map.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_motif_text_map.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_motif_text_map.md'}")


if __name__ == "__main__":
    main()
