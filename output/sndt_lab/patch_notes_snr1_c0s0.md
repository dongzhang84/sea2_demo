# SNDT Lab Patch Notes

This lab artifact preserves the SNDT container and dispatch table,
but replaces one subscript bytecode area with a minimal known program.

## Target

- SNDT file: `Snr1.dat`
- Chunk: `0`
- Subscript: `0`
- Text id: `0`
- Subscript range: `0x0032..0x086e`
- Code start: `0x005e`
- Code length: `2064` bytes

## Program

```text
0c <text_id> f2
```

- Program bytes: `0c 00 f2`
- Original head: `ad 00 01 2a ac 05 00 40 c0 01 cc 00 06 c8 00 00 c7 fe 02 62 ad 05 01 2a ac 01 01 08 0f 01 07 8e`
- Patched head: `0c 00 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2`

## Outputs

- Patched DAT: `output/sndt_lab/Snr1_min_text_c0s0.dat`
- Rebuilt archive: `output/sndt_lab/SNRDAT_min_snr1_c0s0.LZW`

These files are not copied into `game_dos/` automatically.
