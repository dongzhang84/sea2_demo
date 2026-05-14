#!/usr/bin/env python3
"""Extract remaining .dat files in Koukai2/ that we haven't covered:
   Transit.dat, Hdat.put, End_put.dat, Menu.dat, Colony.dat.
   Saves to output/game_data/.
"""
import json
from pathlib import Path
from collections import Counter

KOUKAI = Path('/Users/dong/Projects/Koukai2')
OUT = Path(__file__).resolve().parent.parent / 'output' / 'game_data'


def detect_alignment(raw: bytes) -> int:
    for align in [4, 2, 8]:
        if len(raw) % align != 0:
            continue
        all_zero = all(raw[i] == 0 for i in range(align - 1, len(raw), align))
        if all_zero:
            return align
    return 1


def analyze(raw: bytes, name: str) -> dict:
    n = len(raw)
    align = detect_alignment(raw)
    factors = []
    for s in [4, 8, 12, 16, 24, 32, 48, 64, 96, 100, 128, 138, 160, 177, 240]:
        if n % s == 0:
            count = n // s
            if 5 <= count <= 5000:
                factors.append((count, s))

    result = {
        'source': name,
        'size_bytes': n,
        'alignment': align,
        'pct_zero': round(sum(1 for b in raw if b == 0) / n * 100, 1),
        'pct_ff': round(sum(1 for b in raw if b == 0xff) / n * 100, 1),
        'pct_high_byte': round(sum(1 for b in raw if b >= 0x80) / n * 100, 1),
        'distinct_byte_count': len(set(raw)),
        'first_128_hex': raw[:128].hex(),
        'stride_candidates': [{'records': c, 'stride': s} for c, s in factors[:6]],
    }

    if align == 4:
        triples = [list(raw[i:i+3]) for i in range(0, n, 4)]
        result['as_triples_3bytes_count'] = len(triples)
        result['as_triples_first_50'] = triples[:50]

    # First-record samples for top stride candidates
    structured = {}
    for count, stride in factors[:3]:
        recs = [list(raw[i*stride:(i+1)*stride]) for i in range(min(count, 5))]
        structured[f'{count}x{stride}'] = recs
    result['structured_first_samples'] = structured

    return result


def main():
    files = ['Transit.dat', 'Hdat.put', 'End_put.dat', 'Menu.dat',
             'Colony.dat', 'Event0.dat', 'Snr0.dat', 'Snr1.dat',
             'Snr2.dat', 'Snr3.dat', 'Snr4.dat', 'Snr5.dat', 'Snr6.dat']
    for fname in files:
        p = KOUKAI / fname
        if not p.exists():
            continue
        raw = p.read_bytes()
        result = analyze(raw, fname)
        out = OUT / f'koukai_{fname.replace(".", "_")}.json'
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f'  → {out.name}  size={len(raw):>6}  align={result["alignment"]}'
              f'  %0={result["pct_zero"]:>5.1f}  %FF={result["pct_ff"]:>5.1f}'
              f'  distinct={result["distinct_byte_count"]:>3}')


if __name__ == '__main__':
    main()
