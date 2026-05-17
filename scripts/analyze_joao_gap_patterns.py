#!/usr/bin/env python3
"""Summarize recurring raw byte patterns in João opening non-motif gaps."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GAPS = ROOT / "output" / "sndt_analysis" / "joao_opening_gaps.json"
OUT_DIR = ROOT / "output" / "sndt_analysis"


def byte_values(hex_string: str) -> list[int]:
    if not hex_string:
        return []
    return [int(part, 16) for part in hex_string.split()]


def ngrams(values: list[int], n: int) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for i in range(0, len(values) - n + 1):
        counts[tuple(values[i : i + n])] += 1
    return counts


def fmt_ngram(values: tuple[int, ...]) -> str:
    return " ".join(f"{value:02x}" for value in values)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    gaps = json.loads(GAPS.read_text())["gaps"]
    gap_values = [(gap, byte_values(gap["bytes"])) for gap in gaps]

    byte_counts: Counter[int] = Counter()
    two_counts: Counter[tuple[int, ...]] = Counter()
    three_counts: Counter[tuple[int, ...]] = Counter()
    four_counts: Counter[tuple[int, ...]] = Counter()
    leading_counts: Counter[tuple[int, ...]] = Counter()
    trailing_counts: Counter[tuple[int, ...]] = Counter()
    opcode_like_counts: Counter[int] = Counter()

    for gap, values in gap_values:
        byte_counts.update(values)
        two_counts.update(ngrams(values, 2))
        three_counts.update(ngrams(values, 3))
        four_counts.update(ngrams(values, 4))
        if values:
            leading_counts[tuple(values[: min(4, len(values))])] += 1
            trailing_counts[tuple(values[max(0, len(values) - 4) :])] += 1
        for value in values:
            if value >= 0x80:
                opcode_like_counts[value] += 1

    result = {
        "summary": {
            "gap_count": len(gaps),
            "gap_bytes": sum(len(values) for _, values in gap_values),
        },
        "top_bytes": [{"bytes": f"{value:02x}", "count": count} for value, count in byte_counts.most_common(40)],
        "top_opcode_like_bytes": [
            {"bytes": f"{value:02x}", "count": count} for value, count in opcode_like_counts.most_common(40)
        ],
        "top_2grams": [{"bytes": fmt_ngram(values), "count": count} for values, count in two_counts.most_common(40)],
        "top_3grams": [{"bytes": fmt_ngram(values), "count": count} for values, count in three_counts.most_common(40)],
        "top_4grams": [{"bytes": fmt_ngram(values), "count": count} for values, count in four_counts.most_common(40)],
        "leading_patterns": [{"bytes": fmt_ngram(values), "count": count} for values, count in leading_counts.most_common(40)],
        "trailing_patterns": [{"bytes": fmt_ngram(values), "count": count} for values, count in trailing_counts.most_common(40)],
    }
    (OUT_DIR / "joao_gap_patterns.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# João Gap Byte Pattern Summary",
        "",
        "This summarizes raw byte patterns inside non-motif gaps for `Snr1.chunk0.sub0`.",
        "It is pattern evidence only; these are not confirmed opcode boundaries.",
        "",
        f"- Gaps: `{result['summary']['gap_count']}`",
        f"- Gap bytes: `{result['summary']['gap_bytes']}`",
        "",
        "## Top Opcode-Like Bytes",
        "",
    ]
    for row in result["top_opcode_like_bytes"][:24]:
        lines.append(f"- `{row['bytes']}`: {row['count']}")

    for title, key in [
        ("Top 2-Grams", "top_2grams"),
        ("Top 3-Grams", "top_3grams"),
        ("Top 4-Grams", "top_4grams"),
        ("Leading Gap Patterns", "leading_patterns"),
        ("Trailing Gap Patterns", "trailing_patterns"),
    ]:
        lines += ["", f"## {title}", ""]
        for row in result[key][:24]:
            lines.append(f"- `{row['bytes']}`: {row['count']}")

    lines += ["", "## Initial Pattern Notes", ""]
    lines += [
        "- `fe 02 62` recurs as a compact separator/control-looking sequence between dialogue runs.",
        "- `ad` and `ac` frequently appear near the starts of gaps, likely setup/call-like control opcodes.",
        "- `f8`, `f9`, and `fb` appear in gap control regions and should be prioritized after `ad/ac/fe`.",
        "- Because this report works on raw gaps, repeated `c0/c8/c7` fragments inside long gaps may still be operand-aligned false positives.",
    ]
    (OUT_DIR / "joao_gap_patterns.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'joao_gap_patterns.json'}")
    print(f"Wrote {OUT_DIR / 'joao_gap_patterns.md'}")


if __name__ == "__main__":
    main()
