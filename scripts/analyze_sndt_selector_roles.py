#!/usr/bin/env python3
"""Analyze selector values inside SNDT c0/cc/c8/c7 motif records."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOPOLOGY = ROOT / "output" / "sndt_topology" / "topology_v0_motif.json"
OUT_DIR = ROOT / "output" / "sndt_analysis"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    topology = json.loads(TOPOLOGY.read_text())

    selector_counts: Counter[int] = Counter()
    selector_cc: dict[int, Counter[int]] = defaultdict(Counter)
    selector_speaker: dict[int, Counter[str]] = defaultdict(Counter)
    selector_by_snr: dict[str, Counter[int]] = defaultdict(Counter)
    selector_by_script: dict[str, Counter[int]] = defaultdict(Counter)
    transitions: Counter[tuple[int, int]] = Counter()
    examples: dict[int, list[dict]] = defaultdict(list)
    joao_opening = []

    for file_info in topology["files"]:
        snr = file_info["id"]
        for chunk in file_info["chunks"]:
            for sub in chunk["subscripts"]:
                previous_selector = None
                for run in sub["motif_runs"]:
                    for record in run["records"]:
                        selector = record["selector"]
                        selector_counts[selector] += 1
                        selector_cc[selector][record["cc_arg"]] += 1
                        selector_by_snr[snr][selector] += 1
                        selector_by_script[sub["id"]][selector] += 1
                        speaker = record.get("resolved_speaker")
                        if speaker:
                            selector_speaker[selector][speaker] += 1
                        if previous_selector is not None:
                            transitions[(previous_selector, selector)] += 1
                        previous_selector = selector
                        if len(examples[selector]) < 30:
                            examples[selector].append(
                                {
                                    "script": sub["id"],
                                    "offset_hex": record["offset_hex"],
                                    "cc_arg": record["cc_arg"],
                                    "speaker": speaker,
                                    "text_id": record["text_id"],
                                    "text": record["text_preview"],
                                }
                            )
                        if sub["id"] == "Snr1.chunk0.sub0":
                            joao_opening.append(
                                {
                                    "offset_hex": record["offset_hex"],
                                    "selector": selector,
                                    "cc_arg": record["cc_arg"],
                                    "speaker": speaker,
                                    "text_id": record["text_id"],
                                    "text": record["text_preview"],
                                }
                            )

    result = {
        "summary": {
            "selector_counts": dict(selector_counts.most_common()),
            "transitions": [
                {"from": a, "to": b, "count": count}
                for (a, b), count in transitions.most_common()
            ],
        },
        "selectors": {
            str(selector): {
                "records": selector_counts[selector],
                "top_cc_args": selector_cc[selector].most_common(20),
                "top_speakers": selector_speaker[selector].most_common(20),
                "examples": examples[selector],
            }
            for selector in sorted(selector_counts)
        },
        "by_snr": {
            snr: dict(counts.most_common())
            for snr, counts in sorted(selector_by_snr.items())
        },
        "top_scripts": [
            {"script": script, "selectors": dict(counts.most_common()), "records": sum(counts.values())}
            for script, counts in sorted(selector_by_script.items(), key=lambda item: -sum(item[1].values()))[:60]
        ],
        "joao_opening": joao_opening,
    }
    (OUT_DIR / "sndt_selector_roles.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# SNDT Motif selector Role Analysis",
        "",
        "`selector` is the operand after `c0` in `c0 selector cc cc_arg c8 text_id c7`.",
        "",
        "## Counts",
        "",
    ]
    for selector, count in selector_counts.most_common():
        lines.append(f"- selector `{selector}`: `{count}`")

    lines += ["", "## Transitions Within Subscripts", ""]
    for (a, b), count in transitions.most_common(10):
        lines.append(f"- `{a} -> {b}`: {count}")

    lines += ["", "## By SNDT File", "", "| SNDT | selector 1 | selector 2 |", "|---|---:|---:|"]
    for snr, counts in sorted(selector_by_snr.items()):
        lines.append(f"| {snr} | {counts.get(1, 0)} | {counts.get(2, 0)} |")

    lines += ["", "## Selector Profiles", ""]
    for selector in sorted(selector_counts):
        lines += [
            f"### Selector {selector}",
            "",
            "Top cc_arg values:",
            "",
        ]
        for cc_arg, count in selector_cc[selector].most_common(12):
            lines.append(f"- `cc={cc_arg}`: {count}")
        lines += ["", "Top resolved speakers:", ""]
        for speaker, count in selector_speaker[selector].most_common(12):
            lines.append(f"- `{speaker}`: {count}")
        lines += ["", "Examples:", ""]
        for example in examples[selector][:16]:
            speaker = example["speaker"] or "-"
            lines.append(
                f"- `{example['script']}:{example['offset_hex']}` cc={example['cc_arg']} "
                f"speaker={speaker} text={example['text_id']}: {example['text']}"
            )
        lines.append("")

    lines += ["## João Opening Selector Trace", ""]
    for entry in joao_opening[:180]:
        speaker = entry["speaker"] or "-"
        lines.append(
            f"- `{entry['offset_hex']}` sel={entry['selector']} cc={entry['cc_arg']} "
            f"speaker={speaker} text={entry['text_id']}: {entry['text']}"
        )

    lines += ["", "## Initial Interpretation", ""]
    lines += [
        "- `selector=1` and `selector=2` are nearly balanced globally, so the field is structural rather than incidental data.",
        "- `selector=2` is strongly associated with `cc_arg=0`, but also appears for non-player actor slots such as João opening `cc=31` for Rocco.",
        "- `selector=1` is common for explicit NPC speaker slots and one-line ambient/status prompts.",
        "- Current safe name: `dialogue_selector`, not `speaker_side`; runtime validation is still needed before assigning UI or branch semantics.",
    ]
    (OUT_DIR / "sndt_selector_roles.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_selector_roles.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_selector_roles.md'}")


if __name__ == "__main__":
    main()
