#!/usr/bin/env python3
"""Phase 1: Extract numeric .dat files into structured JSON.

Targets the SMALLEST numeric files first (highest confidence per byte):
  - Za_dat.dat (2424 B = 101 × 24): per-port stats
  - Monster.dat (200 B): sea monster stats
  - Windcur.dat (1350 B): wind/current model

Output to output/game_data/<name>.json with both:
  - raw byte interpretation (u8 array)
  - structured u16 LE / u16 BE candidates
  - 0xFFFF sentinel detection

These extractions are RAW STRUCTURE — semantic field names (what each
column means: price/quantity/region/etc.) require cross-validation
with the game running in DOSBox, which is a separate step.
"""
import json
from pathlib import Path

import numpy as np

KOUKAI = Path('/Users/dong/Projects/Koukai2')
OUT = Path(__file__).resolve().parent.parent / 'output' / 'game_data'
OUT.mkdir(parents=True, exist_ok=True)


def extract_za_dat():
    """Za_dat.dat: 101 records × 24 bytes. 12 u16 LE per port."""
    raw = (KOUKAI / 'Za_dat.dat').read_bytes()
    N = 101
    STRIDE = 24
    assert len(raw) == N * STRIDE

    ports = []
    for i in range(N):
        rec = raw[i * STRIDE:(i + 1) * STRIDE]
        u16_le = [int.from_bytes(rec[k:k + 2], 'little') for k in range(0, STRIDE, 2)]
        u8_vals = list(rec)
        ports.append({
            'port_id': i,
            'u16_le_fields': u16_le,
            'u8_bytes': u8_vals,
            'raw_hex': rec.hex(),
            'sentinel_ffff_count': sum(1 for v in u16_le if v == 0xffff),
        })

    # Stats summary
    field_stats = []
    for f in range(12):
        vals = [p['u16_le_fields'][f] for p in ports]
        non_sentinel = [v for v in vals if v != 0xffff]
        field_stats.append({
            'field_index': f,
            'byte_offset': f * 2,
            'distinct_values': len(set(vals)),
            'sentinel_count': sum(1 for v in vals if v == 0xffff),
            'non_sentinel_min': min(non_sentinel) if non_sentinel else None,
            'non_sentinel_max': max(non_sentinel) if non_sentinel else None,
            'non_sentinel_mean': round(sum(non_sentinel) / len(non_sentinel), 1) if non_sentinel else None,
        })

    return {
        'source': 'Za_dat.dat',
        'description': 'Per-port stats. 101 records × 24 bytes = 12 u16 LE each.'
                      ' Last 7 fields can hold 0xFFFF as "not applicable" sentinel.',
        'record_count': N,
        'record_size_bytes': STRIDE,
        'fields_per_record': 12,
        'field_stats': field_stats,
        'ports': ports,
    }


def extract_monster_dat():
    """Monster.dat: 200 bytes. Probe stride."""
    raw = (KOUKAI / 'Monster.dat').read_bytes()
    print(f'Monster.dat: {len(raw)} bytes')
    print(f'  hex: {raw.hex()}')

    # Common factorizations: 200 = 10*20 = 20*10 = 25*8 = 8*25 = 40*5 = 50*4
    result = {'source': 'Monster.dat', 'size_bytes': len(raw), 'raw_hex': raw.hex()}
    for n_records, stride in [(10, 20), (20, 10), (25, 8), (40, 5), (8, 25), (50, 4)]:
        if n_records * stride == len(raw):
            records = []
            for i in range(n_records):
                rec = raw[i * stride:(i + 1) * stride]
                records.append({
                    'id': i, 'bytes': list(rec),
                    'u16_le': [int.from_bytes(rec[k:k+2], 'little')
                              for k in range(0, stride, 2)] if stride % 2 == 0 else None,
                })
            result[f'as_{n_records}x{stride}'] = {
                'n_records': n_records,
                'stride': stride,
                'records': records,
            }
    return result


def extract_windcur_dat():
    """Windcur.dat: 1350 bytes. Likely grid representing world wind/current."""
    raw = (KOUKAI / 'Windcur.dat').read_bytes()
    print(f'Windcur.dat: {len(raw)} bytes')

    # 1350 = 2 × 27 × 25 = 30 × 45 = 27 × 50 = 25 × 54 = 54 × 25 etc.
    # Worldmap is 30 cols × 45 rows = 1350. PERFECT MATCH!
    # So Windcur.dat is likely 30×45 = 1350 byte grid (1 byte per "world block")
    if len(raw) == 1350:
        grid_30x45 = np.frombuffer(raw, dtype=np.uint8).reshape(45, 30)
        # Each byte's value distribution
        from collections import Counter
        c = Counter(raw)
        return {
            'source': 'Windcur.dat',
            'size_bytes': len(raw),
            'grid_layout': '30 cols × 45 rows (matches worldmap block structure)',
            'distinct_values': dict(sorted(c.items())),
            'grid_30x45': grid_30x45.tolist(),
        }
    return {'source': 'Windcur.dat', 'size_bytes': len(raw)}


def main():
    for fn, name in [
        (extract_za_dat, 'za_dat'),
        (extract_monster_dat, 'monster_dat'),
        (extract_windcur_dat, 'windcur_dat'),
    ]:
        result = fn()
        p = OUT / f'{name}.json'
        p.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f'→ {p}  ({p.stat().st_size:,} B)')


if __name__ == '__main__':
    main()
