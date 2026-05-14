#!/usr/bin/env python3
"""Bulk-extract Data1.lzw remaining parts to JSON dumps.

Phase 1 = collect structured data. Semantic understanding (what each byte means)
comes in Phase 2 by cross-referencing with Main.exe disassembly.

For each part, try multiple stride hypotheses and dump the most plausible.
"""
import json
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent
PARTS = REPO / 'output' / 'lzw_parts' / 'Data1'
OUT = REPO / 'output' / 'game_data'
OUT.mkdir(parents=True, exist_ok=True)

# Already-known parts (skip)
KNOWN = {'part_0010_512bytes.bin', 'part_0011_32768bytes.bin', 'part_0018_1024bytes.bin'}


def detect_alignment(raw: bytes) -> int:
    """Detect if data has N-byte alignment (Nth byte always 0).
    Returns the alignment size (1=no alignment, 4=common KOEI pattern)."""
    for align in [4, 2, 8]:
        if len(raw) % align != 0:
            continue
        # Check if every align-th byte is 0
        all_zero = all(raw[i] == 0 for i in range(align - 1, len(raw), align))
        if all_zero:
            return align
    return 1


def analyze(raw: bytes, name: str) -> dict:
    n = len(raw)
    align = detect_alignment(raw)

    # Strides to try based on file size
    factors = []
    for s in [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]:
        if n % s == 0:
            count = n // s
            if 10 <= count <= 5000:
                factors.append((count, s))

    result = {
        'source': name,
        'size_bytes': n,
        'alignment': align,
        'byte_histogram': {f'0x{k:02x}': v for k, v in sorted(Counter(raw).items())},
        'pct_zero': round(sum(1 for b in raw if b == 0) / n * 100, 1),
        'pct_ff': round(sum(1 for b in raw if b == 0xff) / n * 100, 1),
        'stride_candidates': [{'records': c, 'stride': s} for c, s in factors[:5]],
        'first_64_hex': raw[:64].hex(),
    }

    # If alignment=4, dump as triples
    if align == 4:
        triples = []
        for i in range(0, n, 4):
            t = list(raw[i:i+3])  # 3 data bytes
            triples.append(t)
        result['as_triples_3bytes'] = {
            'count': len(triples),
            'triples': triples[:200],  # cap to first 200 for size
        }
        result['triples_total'] = len(triples)

    # For each plausible stride, dump first 5 records' bytes
    structured = {}
    for count, stride in factors[:4]:
        recs = [list(raw[i*stride:(i+1)*stride]) for i in range(count)]
        structured[f'{count}x{stride}'] = {
            'first_records': recs[:5],
        }
    result['structured_attempts'] = structured

    return result


def main():
    parts = sorted(PARTS.glob('*.bin'))
    inventory = []
    for p in parts:
        if p.name in KNOWN:
            inventory.append({'file': p.name, 'status': 'previously known'})
            continue
        raw = p.read_bytes()
        result = analyze(raw, p.name)
        out_path = OUT / f'data1_{p.name.replace(".bin", ".json")}'
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f'  → {out_path.name}  ({out_path.stat().st_size:,} B)  align={result["alignment"]}  '
              f'%0={result["pct_zero"]:.1f}  %FF={result["pct_ff"]:.1f}')
        inventory.append({
            'file': p.name,
            'size': len(raw),
            'alignment': result['alignment'],
            'pct_zero': result['pct_zero'],
            'pct_ff': result['pct_ff'],
            'stride_candidates': result['stride_candidates'],
        })

    # Write summary
    summary_path = OUT / 'data1_inventory.json'
    summary_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False))
    print(f'\n→ summary: {summary_path}')


if __name__ == '__main__':
    main()
