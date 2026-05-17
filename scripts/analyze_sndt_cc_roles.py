#!/usr/bin/env python3
"""Cluster motif cc_arg values by script, selector, and mapped dialogue text."""
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
MOTIF_RECORDS = OUT_DIR / "sndt_motif_records.json"

sys.path.insert(0, str(ROOT / "scripts"))
from decode_text import decode_file  # noqa: E402


SNR_RE = re.compile(r"Snr(\d+)\.")
SPEAKER_RE = re.compile(r"^〔([^〕]+)〕")


def snr_id_for_script(script: str) -> int:
    match = SNR_RE.match(script)
    if not match:
        raise ValueError(script)
    return int(match.group(1))


def one_line(text: str, limit: int = 96) -> str:
    text = text.replace("\n", "\\n")
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def speaker_for_text(text: str) -> str | None:
    match = SPEAKER_RE.match(text)
    if not match:
        return None
    return match.group(1)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    motif = json.loads(MOTIF_RECORDS.read_text())
    texts = {snr_id: decode_file(str(KOUKAI / f"Snr{snr_id}.mes")) for snr_id in range(7)}

    records_with_text = []
    speaker_hints: dict[tuple[str, int], Counter[str]] = defaultdict(Counter)
    for record in motif["records"]:
        script = record["script"]
        snr_id = snr_id_for_script(script)
        text_id = record["c8_arg"]
        text = texts[snr_id][text_id] if 0 <= text_id < len(texts[snr_id]) else ""
        speaker = speaker_for_text(text)
        if speaker:
            speaker_hints[(script, record["cc_arg"])][speaker] += 1
        records_with_text.append((record, text, speaker))

    cc_groups: dict[int, dict] = defaultdict(
        lambda: {
            "records": 0,
            "selectors": Counter(),
            "scripts": Counter(),
            "snrs": Counter(),
            "explicit_speakers": Counter(),
            "resolved_speakers": Counter(),
            "examples": [],
        }
    )
    joao_opening = []

    for record, text, speaker in records_with_text:
        script = record["script"]
        snr_id = snr_id_for_script(script)
        text_id = record["c8_arg"]
        cc_arg = record["cc_arg"]
        resolved_speaker = speaker
        if not resolved_speaker and speaker_hints.get((script, cc_arg)):
            resolved_speaker = speaker_hints[(script, cc_arg)].most_common(1)[0][0]
        group = cc_groups[cc_arg]
        group["records"] += 1
        group["selectors"][record["selector"]] += 1
        group["scripts"][script] += 1
        group["snrs"][f"Snr{snr_id}"] += 1
        if speaker:
            group["explicit_speakers"][speaker] += 1
        if resolved_speaker:
            group["resolved_speakers"][resolved_speaker] += 1
        if len(group["examples"]) < 12:
            group["examples"].append(
                {
                    "script": script,
                    "offset_hex": record["offset_hex"],
                    "selector": record["selector"],
                    "text_id": text_id,
                    "resolved_speaker": resolved_speaker,
                    "text": one_line(text),
                }
            )
        if script == "Snr1.chunk0.sub0":
            joao_opening.append(
                {
                    "offset_hex": record["offset_hex"],
                    "selector": record["selector"],
                    "cc_arg": cc_arg,
                    "text_id": text_id,
                    "speaker": speaker,
                    "resolved_speaker": resolved_speaker,
                    "text": one_line(text),
                }
            )

    groups = []
    for cc_arg, group in sorted(cc_groups.items(), key=lambda item: (-item[1]["records"], item[0])):
        explicit_speakers = group["explicit_speakers"].most_common(10)
        resolved_speakers = group["resolved_speakers"].most_common(10)
        groups.append(
            {
                "cc_arg": cc_arg,
                "records": group["records"],
                "selectors": dict(group["selectors"].most_common()),
                "snrs": dict(group["snrs"].most_common()),
                "top_scripts": group["scripts"].most_common(12),
                "explicit_speakers": explicit_speakers,
                "resolved_speakers": resolved_speakers,
                "resolved_speaker_ratio": (
                    sum(count for _, count in resolved_speakers) / group["records"] if group["records"] else 0
                ),
                "examples": group["examples"],
            }
        )

    result = {
        "summary": {
            "cc_arg_count": len(groups),
            "motif_records": motif["record_count"],
        },
        "groups": groups,
        "joao_opening": joao_opening,
    }
    (OUT_DIR / "sndt_cc_roles.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

    lines = [
        "# SNDT Motif cc_arg Role Clusters",
        "",
        "`cc_arg` appears inside the motif `c0 selector cc cc_arg c8 text_id c7`.",
        "This report clusters each value by selector distribution, SNDT file, speaker prefix, and example text.",
        "",
        f"- Distinct cc_arg values: `{len(groups)}`",
        f"- Motif records: `{motif['record_count']}`",
        "",
        "## Top cc_arg Values",
        "",
        "| cc_arg | records | selectors | resolved speakers | top scripts |",
        "|---:|---:|---|---|---|",
    ]
    for group in groups[:40]:
        speakers = ", ".join(f"{name}({count})" for name, count in group["resolved_speakers"][:4]) or "-"
        scripts = ", ".join(f"{script}({count})" for script, count in group["top_scripts"][:4])
        lines.append(
            f"| {group['cc_arg']} | {group['records']} | {group['selectors']} | {speakers} | {scripts} |"
        )

    lines += ["", "## João Opening cc_arg Map", ""]
    for entry in joao_opening[:180]:
        speaker = entry["speaker"] or entry["resolved_speaker"] or "-"
        lines.append(
            f"- `{entry['offset_hex']}` sel={entry['selector']} cc={entry['cc_arg']} "
            f"text={entry['text_id']} speaker={speaker}: {entry['text']}"
        )

    lines += ["", "## Initial Interpretation", ""]
    lines += [
        "- `cc_arg=0` is dominated by selector 2 and usually has no explicit `〔speaker〕` prefix; it likely marks the player/protagonist side or a default self-line.",
        "- Non-zero `cc_arg` values often line up with named speaker prefixes in localized text, but not one-to-one globally.",
        "- In João opening, `cc_arg=18`, `19`, `31`, `32`, `97`, and `98` behave like local actor/state slots around the current event scene.",
        "- Therefore `cc_arg` is best treated as a local dialogue actor/state slot until runtime evidence separates character id from condition id.",
    ]
    (OUT_DIR / "sndt_cc_roles.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {OUT_DIR / 'sndt_cc_roles.json'}")
    print(f"Wrote {OUT_DIR / 'sndt_cc_roles.md'}")


if __name__ == "__main__":
    main()
