# João Gap Byte Pattern Summary

This summarizes raw byte patterns inside non-motif gaps for `Snr1.chunk0.sub0`.
It is pattern evidence only; these are not confirmed opcode boundaries.

- Gaps: `41`
- Gap bytes: `804`

## Top Opcode-Like Bytes

- `c0`: 47
- `c8`: 47
- `c7`: 47
- `ac`: 31
- `ad`: 22
- `f8`: 12
- `dc`: 11
- `f2`: 10
- `fe`: 9
- `8c`: 9
- `8f`: 4
- `cb`: 3
- `fb`: 2
- `c4`: 2
- `d9`: 2
- `e8`: 2
- `e6`: 2
- `f4`: 2
- `b8`: 2
- `f0`: 2
- `8d`: 2
- `c6`: 2
- `bc`: 2
- `eb`: 2

## Top 2-Grams

- `c0 00`: 47
- `00 c8`: 47
- `c8 00`: 47
- `c7 c0`: 17
- `00 01`: 13
- `00 03`: 12
- `ad 00`: 9
- `dc 00`: 9
- `ac 00`: 9
- `1d 00`: 7
- `00 07`: 7
- `02 62`: 6
- `0c 3f`: 6
- `3f 00`: 6
- `00 05`: 6
- `07 48`: 6
- `8c 00`: 6
- `fe 02`: 5
- `05 01`: 5
- `f8 f2`: 5
- `f2 ac`: 5
- `f8 ad`: 5
- `c7 f8`: 5
- `c7 ac`: 5

## Top 3-Grams

- `c0 00 c8`: 47
- `00 c8 00`: 47
- `c7 c0 00`: 17
- `0c 3f 00`: 6
- `3f 00 01`: 6
- `fe 02 62`: 5
- `f8 ad 00`: 5
- `f2 ac 00`: 4
- `07 48 ac`: 4
- `fe 07 48`: 4
- `f8 f2 ac`: 3
- `1d 00 64`: 3
- `c7 ad 00`: 3
- `f2 0c 3f`: 3
- `00 01 ac`: 3
- `01 ac 00`: 3
- `c7 ac 07`: 3
- `dc 00 03`: 3
- `ad 00 07`: 3
- `c7 f8 ad`: 3
- `c7 8c 00`: 3
- `01 2a ac`: 2
- `02 62 ad`: 2
- `dc 00 06`: 2

## Top 4-Grams

- `c0 00 c8 00`: 47
- `c7 c0 00 c8`: 17
- `0c 3f 00 01`: 6
- `f8 f2 ac 00`: 3
- `f2 0c 3f 00`: 3
- `3f 00 01 ac`: 3
- `00 01 ac 00`: 3
- `fe 07 48 ac`: 3
- `c7 f8 ad 00`: 3
- `fe 02 62 ad`: 2
- `dc 00 06 00`: 2
- `00 06 00 3f`: 2
- `01 fe 02 62`: 2
- `01 f8 ad 00`: 2
- `0c 00 03 e8`: 2
- `00 03 e8 e6`: 2
- `03 e8 e6 00`: 2
- `0f 1d 00 64`: 2
- `01 f8 f2 ac`: 2
- `c7 f8 f2 0c`: 2
- `f8 f2 0c 3f`: 2
- `f4 c0 00 c8`: 2
- `c7 ac 07 04`: 2
- `01 c0 00 c8`: 2

## Leading Gap Patterns

- `c0 00 c8 00`: 9
- `fe 02 62 ad`: 2
- `0c 00 03 e8`: 2
- `fe 07 48 ac`: 2
- `ad 00 01 2a`: 1
- `dc 00 06 00`: 1
- `fe 02 62 ac`: 1
- `f9 05 05`: 1
- `fb 45 2c 00`: 1
- `ac 04 02 be`: 1
- `c4 ca 04`: 1
- `2c 04 01 f8`: 1
- `f8 ac 05 03`: 1
- `c4`: 1
- `dc 00 05 00`: 1
- `2c 07 01 f8`: 1
- `fb 46`: 1
- `dc 00 0c 62`: 1
- `ad 07 05 f0`: 1
- `f8 fe 07 48`: 1
- `ad 08 06 16`: 1
- `ad 05 06 23`: 1
- `dc 0b 03 46`: 1
- `e9 0b ad 0b`: 1

## Trailing Gap Patterns

- `0c 3f 00 01`: 2
- `ac 05 00 40`: 1
- `01 42 00 f7`: 1
- `01 41 01 08`: 1
- `ad 01 01 2a`: 1
- `ac 00 02 62`: 1
- `f9 05 05`: 1
- `ad 04 02 75`: 1
- `ac 04 02 be`: 1
- `c4 ca 04`: 1
- `03 e8 e6 00`: 1
- `c4`: 1
- `c8 00 5a c7`: 1
- `c8 00 5d c7`: 1
- `01 00 04 53`: 1
- `01 01 04 7b`: 1
- `01 02 04 8f`: 1
- `ac 07 04 ac`: 1
- `ad 07 04 cb`: 1
- `c8 00 6f c7`: 1
- `c8 00 73 c7`: 1
- `fb 46`: 1
- `c8 00 7d c7`: 1
- `ad 00 05 a2`: 1

## Initial Pattern Notes

- `fe 02 62` recurs as a compact separator/control-looking sequence between dialogue runs.
- `ad` and `ac` frequently appear near the starts of gaps, likely setup/call-like control opcodes.
- `f8`, `f9`, and `fb` appear in gap control regions and should be prioritized after `ad/ac/fe`.
- Because this report works on raw gaps, repeated `c0/c8/c7` fragments inside long gaps may still be operand-aligned false positives.
