# SNDT Lab Patch Notes

This lab artifact preserves the SNDT container and dispatch table,
but replaces one subscript bytecode area with a minimal known program.

## Target

- SNDT file: `Snr4.dat`
- Chunk: `0`
- Subscript: `0`
- Text id: `0`
- Subscript range: `0x002e..0x01fb`
- Code start: `0x004a`
- Code length: `433` bytes

## Program

```text
0c <text_id> f2
```

- Program bytes: `0c 00 f2`
- Original head: `c0 01 cc 00 0f c8 00 00 c7 c0 01 cc 00 0f c8 00 01 c7 c0 02 cc 00 03 c8 00 02 c7 c0 02 cc 00 03`
- Patched head: `0c 00 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2 f2`

## Outputs

- Patched DAT: `output/sndt_lab/Snr4_min_text_c0s0.dat`
- Rebuilt archive: `output/sndt_lab/SNRDAT_min_snr4_c0s0.LZW`

These files are not copied into `game_dos/` automatically.
