# SNDT Opcode Table

> This table tracks confirmed and candidate SNDT bytecode opcodes.
> It is intentionally conservative: confirmed entries require direct evidence;
> candidate entries are based on repeated static motifs and still need runtime validation.

## Status Legend

| Status | Meaning |
|---|---|
| confirmed | Verified by text flow or structural terminator evidence |
| strong-candidate | Strong static motif evidence, not yet runtime-confirmed |
| unknown | Seen in bytecode but length/semantics not established |

---

## Confirmed

| Opcode | Length | Name | Evidence |
|---|---:|---|---|
| `0x0c` | 2 | `show_text(text_id)` | `0c XX` references valid `Snr*.mes` entries; Snr0 task dialogue reads coherently |
| `0xf2` | 1 | `end_subscript` | Subscript bytecode areas terminate with `f2` |

---

## Strong Candidates

These are supported by `output/sndt_analysis/sndt_motifs.md`.

The repeated motif:

```text
c0 ?? cc ?? ?? c8 ?? ?? c7
```

appears 3449 times across 186 code areas. The alignment strongly suggests:

| Opcode | Candidate Length | Candidate Role | Evidence |
|---|---:|---|---|
| `0xc0` | 2 | small selector / condition setup | Motif prefix `c0 01` / `c0 02` repeats heavily |
| `0xcc` | 3 | load/compare immediate or state id | Appears as `cc 00 xx` inside the motif |
| `0xc8` | 3 | motif text id | In all 3449 motif records, `c8_arg` maps to a valid matching `Snr*.mes` text id |
| `0xc7` | 1 | separator / commit / end-record | Ends each repeated motif record |

The `0xc8` operand is now strongly tied to text: `output/sndt_analysis/sndt_motif_text_map.md`
maps all 3449 motif records to valid `Snr*.mes` entries with no unmapped records.
The remaining unknowns are the control meaning of `c0`, `cc`, and `c7`, plus whether
`0xc8` is also used outside this motif.

---

## High-Priority Unknowns

| Opcode | Current Notes |
|---|---|
| `0xad` | Appears near Snr1 opening code before the repeated `c0/cc/c8/c7` table |
| `0xac` | Often appears near `0xad`; likely part of setup or call sequence |
| `0xfe` | Seen near Snr1 opening code; may be control/branch-related |
| `0xa3` | Appears as dispatch table tag in Snr0; bytecode role not confirmed |
| `0xdc` | Previously observed in raw opcode notes; not length-known |
| `0x8c` | Previously observed with 4-byte-looking records; not length-known |

---

## Next Validation Step

Use these candidate lengths to write a partial disassembler that only recognizes:

```text
0x0c len 2
0xf2 len 1
0xc0 len 2
0xcc len 3
0xc8 len 3
0xc7 len 1
```

Then test whether the repeated motif areas decode cleanly and whether `0x0c` text references become less noisy.

Runtime validation is still required before treating `0xc0/0xcc/0xc7` semantics as real.
For the motif form, `0xc8` should be treated as a text id unless contradictory runtime
evidence appears.
