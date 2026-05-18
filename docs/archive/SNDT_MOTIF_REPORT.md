# SNDT Motif Report

> This report summarizes the current static evidence for the repeated
> `c0/cc/c8/c7` structure inside SNDT bytecode.

## Summary

The byte pattern:

```text
c0 <selector> cc <u16> c8 <u16> c7
```

appears **3449** times across the 7 SNDT files. These records form **977**
contiguous runs. Many runs have `c8_arg` increasing by exactly 1, which strongly
suggests this is not accidental byte noise.

Current interpretation:

```text
c0 selector     dialogue selector / channel candidate, currently only 1 or 2
cc u16          local actor/state slot candidate
c8 u16          text id into the matching Snr*.mes file
c7              record terminator / commit
```

The `c8` part is backed by full text-map evidence. `cc_arg` now has strong
speaker/actor-slot evidence in João opening, and `selector` has strong dialogue
alternation evidence. Runtime validation is still required before using the `c0`,
`cc`, and `c7` names as final opcode semantics.

## Key Facts

| Metric | Value |
|---|---:|
| Motif records | 3449 |
| Contiguous runs | 977 |
| Selector 1 records | 1728 |
| Selector 2 records | 1721 |
| Records whose `c8_arg` maps to matching `.mes` text | 3449 |
| Unmapped `c8_arg` records | 0 |

The selector split is almost exactly balanced:

```text
selector 1: 1728
selector 2: 1721
```

This strongly suggests `selector` is a binary class or mode, not arbitrary data.

`output/sndt_analysis/sndt_selector_roles.md` adds one important constraint:
`selector` is not simply "player versus NPC". In João opening, `selector=2`
is often João when `cc_arg=0`, but it can also be Rocco or Enrique when the
local actor slot changes. The safe static name is therefore `dialogue_selector`.

## Text Map Evidence

`output/sndt_analysis/sndt_motif_text_map.md` checks every motif record against
the matching `Snr*.mes` file. The result is:

```text
3449 / 3449 motif records map to valid text ids
0 unmapped records
```

Per-file coverage is also complete for every protagonist file that has motif records:

```text
Snr1 1070/1070
Snr2  853/853
Snr3  456/456
Snr4  218/218
Snr5  251/251
Snr6  601/601
```

This upgrades `c8_arg` from "likely table index" to "motif text id". It also
means the motif topology can attach real dialogue lines to internal event records.

## Actor Slot Evidence

`output/sndt_analysis/sndt_cc_roles.md` clusters all 41 distinct `cc_arg` values.
Several values resolve cleanly in João opening:

```text
cc=18 -> $s公爵
cc=31 -> 老水手洛克
cc=32 -> 恩里克神父
cc=97 -> 紅鯨亭女老闆卡蕾珞娃
cc=98 -> 歌女路琪亞
cc=0  -> mostly João / protagonist self lines
```

This means the motif record now carries usable static dialogue metadata:

```text
selector + cc_arg + text_id -> speaker-ish text edge
```

The exact runtime role of `cc_arg` is still not final. It may be an actor slot,
a condition slot, or a combined state-dependent dialogue slot.

## Longest Runs

The longest contiguous run is:

```text
Snr5.chunk3.sub2:0x0105..0x02e2
count=53
selectors=[1, 2]
cc=[4, 22]
c8=265..317
c8 step +1 = true
```

Other long runs also show `c8_arg` as a continuous range:

```text
Snr2.chunk5.sub0 count=42 c8=408..449
Snr2.chunk7.sub2 count=36 c8=757..792
Snr6.chunk2.sub4 count=33 c8=483..515
Snr1.chunk0.sub0 count=28 c8=22..49
```

This points toward a table-like structure:

```text
record 0 -> c8 index N
record 1 -> c8 index N+1
record 2 -> c8 index N+2
...
```

## João Opening Script

`Snr1.chunk0.sub0`, the João opening script area, has **140** motif records.

Important runs include:

```text
Snr1.chunk0.sub0:0x0024..0x00bd
count=17
selectors=[1, 2]
cc=[0, 19, 31]
c8=1..17
step1=true

Snr1.chunk0.sub0:0x0102..0x01fe
count=28
selectors=[1, 2]
cc=[0, 18]
c8=22..49
step1=true
```

This makes `Snr1.chunk0.sub0` a good target for manual topology reconstruction:
it has known opening text and dense structured records.

## Current Topology Meaning

Before this report, the known topology was mostly:

```text
file -> chunk -> subscript -> dispatch table -> bytecode
```

Now we can add a likely internal table layer:

```text
subscript bytecode
  -> motif run
    -> motif record(selector, cc_arg, c8_arg)
```

In topology terms, these runs are probably not linear prose. They look like
state-index tables or condition-index tables used by the VM to choose what to do.

## What This Does Not Prove Yet

This report does not prove:

- the exact UI/runtime meaning of `selector=1` versus `selector=2`
- whether every `cc_arg` is an actor slot, or whether some are flags/conditions/state ids
- whether `c7` is truly a terminator or an action opcode

It proves that the repeated structure is real enough to guide the next
disassembler and topology extraction pass, and that `c8_arg` is usable as a
dialogue/text edge label in the current topology.

## Next Step

The next useful tool should merge motif runs into the partial disassembly:

```text
motif_run {
  records: [
    {selector, cc_arg, c8_arg},
    ...
  ]
}
```

Then the topology extractor can treat motif runs as first-class nodes instead
of isolated opcodes.

Target outputs:

```text
output/sndt_analysis/sndt_motif_records.json
output/sndt_topology/topology_v0_motif.json
output/sndt_topology/topology_v0_motif.dot
```
