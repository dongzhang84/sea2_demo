# João Opening Edge Validation Targets

This note narrows the João opening topology v1 down to the control edges that are
worth validating first in a debugger or patch experiment.

The current topology export is here:

- [joao_opening_topology_v1.json](/Users/dong/Projects/sea2_demo/output/sndt_topology/joao_opening_topology_v1.json)
- [joao_opening_topology_v1.dot](/Users/dong/Projects/sea2_demo/output/sndt_topology/joao_opening_topology_v1.dot)

## Why these edges

The control-edge analyzer found 68 candidate control instructions in the João opening.
Under the preferred interpretation, 63 of them land on, inside, or near an existing
timeline item. The highest-value next step is not to keep expanding the static graph,
but to validate the few edges that already look like real control transfers.

## Priority Targets

### 1. `fe 07 48`

- Seen at `0x059d`, `0x05c5`, `0x05f7`, `0x070d`
- Maps exactly to short text `172` start at `0x0748`
- Repeated exact-start hits make this the cleanest target-bearing control form in the slice

### 2. `ad 00 07 48`

- Seen at `0x058c`
- Also maps exactly to `0x0748`
- This is the cleanest `ad` sample and the best candidate for a branch/call-style transfer

### 3. `ac 00 08 07`

- Seen at `0x079f`
- Lands exactly on short text `188` start at `0x0807`
- This is valuable because it is close to the end of the João slice, where edge conditions are easiest to see

### 4. `ad 00 03 e0`

- Seen at `0x03aa`
- Lands inside the short text span for text `92`
- Good for checking whether the target is a real jump into a text-bearing block or just a nearby setup operand

### 5. `ac 00 03 d6`

- Seen at `0x03a0`
- Lands inside the João default-line scene around `0x03d6`
- Useful because it sits in a dense region where false positives would be obvious

### 6. `8c 00 01 07 f5`

- Seen at `0x07b8`
- Lands inside the final João scene block
- This is the best `8c` sample that still appears to point into real script structure rather than noise

### 7. `8c 00 00 07 e4`

- Seen at `0x07a7`
- Near short text `185`
- Useful as a boundary case: if this resolves in runtime, it likely confirms `8c` as a structured control form

### 8. `ac 01 02 d9`

- Seen at `0x029b`
- Exact-start hit on the `$s公爵` block
- Important because it suggests the low bytes are not just decorative; they can align with real execution starts

## What to verify

For each target, the debugger should answer:

1. Does execution reach the candidate offset by changing the bytecode pointer?
2. Does the pointer land on the next known item start, or merely pass through the region?
3. Is the operand acting as a direct offset, a relative offset, or a table/index reference?

## Current conclusion

The static evidence is already strong enough to stop treating `ad/ac/8c/fe` as random
residual bytes. The remaining work is to verify which of these are real transfer edges,
which are table lookups, and which are only setup/control-adjacent operands.
