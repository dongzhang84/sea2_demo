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
| `0xc0` | 2 | motif dialogue selector | Motif prefix `c0 01` / `c0 02`; selector counts are nearly balanced and often alternate in dialogue runs |
| `0xcc` | 3 | local actor/state slot | `cc_arg` clusters line up with speaker/actor slots in João opening and other scenes |
| `0xc8` | 3 | motif text id | In all 3449 motif records, `c8_arg` maps to a valid matching `Snr*.mes` text id |
| `0xc7` | 1 | separator / commit / end-record | Ends each repeated motif record |

The `0xc8` operand is now strongly tied to text: `output/sndt_analysis/sndt_motif_text_map.md`
maps all 3449 motif records to valid `Snr*.mes` entries with no unmapped records.
`output/sndt_analysis/sndt_selector_roles.md` shows selector counts of 1728 vs 1721 and
frequent 1/2 alternation inside dialogue runs. The safe current name is
`dialogue_selector`: it is not simply protagonist vs NPC.

`output/sndt_analysis/sndt_cc_roles.md` shows 41 distinct `cc_arg` values. Several map
cleanly to local actor slots in João opening, for example `cc=18` as the duke,
`cc=31` as Rocco, `cc=32` as Enrique, `cc=97` as the tavern owner, and `cc=98`
as Lucia. This may still mix actor slots and state/condition slots in other scenes.

The remaining unknowns are the exact runtime meaning of `c0`, `cc`, and `c7`, plus
whether `0xc8` is also used outside this motif.

---

## Control Edge Candidates

These are supported by the João opening residual-control analysis:

- `output/sndt_analysis/joao_control_candidates.md`
- `output/sndt_analysis/joao_control_disasm.md`
- `output/sndt_analysis/joao_control_edges.md`

The edge analyzer tested 68 control instructions against the 87-item João opening
timeline. Across all operand interpretations it found 25 exact-start matches,
4 exact-end matches, 128 inside-item matches, and 59 near-item matches. Under the
current preferred interpretation, 63/68 instructions land on, inside, or near a
known timeline item.

| Opcode | Candidate Length | Candidate Role | Edge Evidence |
|---|---:|---|---|
| `0xad` | 4 | branch/call/setup with target operand | Big-endian low16/operand forms repeatedly land inside or near João timeline items; `ad 00 07 48` lands exactly on short text 172 at `0x0748` |
| `0xac` | 4 | branch/call/setup with target operand | Often pairs with `0xad`; low16/operand forms repeatedly land inside or near João timeline items; `ac 00 08 07` lands exactly on short text 188 at `0x0807` |
| `0xfe` | 3 | control transfer / separator target | Repeated `fe 02 62` and `fe 07 48`; preferred operand maps 9/9 into code range, including four exact starts |
| `0x8c` | 5 | multi-way branch / indexed target form | Low16 big-endian target form maps several records into or near late João timeline nodes, e.g. `8c 00 00 07 e4` near short text 185 |

This does not yet prove full runtime semantics. It does show that these bytes are
not random residual data: their operands correlate strongly with script offsets.

## High-Priority Unknowns

| Opcode | Current Notes |
|---|---|
| `0xad` | João-slice candidate `len=4`; control-edge evidence is strong, but exact semantic split between branch/call/setup is unknown |
| `0xac` | João-slice candidate `len=4`; control-edge evidence is strong, but exact semantic split between branch/call/setup is unknown |
| `0xfe` | João-slice candidate `len=3`; repeated `fe 02 62` / `fe 07 48` behave like target-bearing control forms |
| `0xf8` | João-slice candidate `len=1`; often appears before `f2`, `ad`, `ac`, or `fe` |
| `0xf9` | João-slice candidate `len=3`; seen as `f9 05 05` in João opening |
| `0xfb` | João-slice candidate `len=2`; seen as `fb 45` / `fb 46` near segment exits |
| `0x8c` | João-slice candidate `len=5`; repeated forms look target-like and may encode indexed/multi-way branches |
| `0xdc` | João-slice candidate `len=4`; clusters with small numeric operands around condition-looking regions |
| `0x2c` | João-slice candidate `len=3`; common before branch/end sequences |
| `0xa3` | Appears as dispatch table tag in Snr0; bytecode role not confirmed |

The João-slice candidates above are supported by `output/sndt_analysis/joao_control_candidates.md`
and `output/sndt_analysis/joao_control_disasm.md`. They are not global confirmations yet.

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

Then merge `joao_control_edges.*` into a João opening topology v1 export, separating
sequence edges from candidate control edges.

Runtime validation is still required before treating `0xc0/0xcc/0xc7` semantics as real.
For the motif form, `0xc8` should be treated as a text id unless contradictory runtime
evidence appears. Runtime validation is also required before assigning final branch/call
semantics to `0xad/0xac/0xfe/0x8c`.
