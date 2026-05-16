# SNDT Motif Analysis

- Code areas: `186`
- Total code bytes: `63801`
- `c0 ?? cc ???? c8 ???? c7` hits: `3449`

## Candidate Length Signal

The structured motif supports this candidate split:

```text
c0 ??        -> candidate len 2
cc ?? ??     -> candidate len 3
c8 ?? ??     -> candidate len 3
c7           -> candidate len 1
```

## First Motif Examples

- `Snr1.chunk0.sub0:0x0008` `c0 01 cc 00 06 c8 00 00 c7`
- `Snr1.chunk0.sub0:0x0024` `c0 01 cc 00 13 c8 00 01 c7`
- `Snr1.chunk0.sub0:0x002d` `c0 02 cc 00 00 c8 00 02 c7`
- `Snr1.chunk0.sub0:0x0036` `c0 02 cc 00 1f c8 00 03 c7`
- `Snr1.chunk0.sub0:0x003f` `c0 02 cc 00 1f c8 00 04 c7`
- `Snr1.chunk0.sub0:0x0048` `c0 01 cc 00 13 c8 00 05 c7`
- `Snr1.chunk0.sub0:0x0051` `c0 02 cc 00 1f c8 00 06 c7`
- `Snr1.chunk0.sub0:0x005a` `c0 02 cc 00 1f c8 00 07 c7`
- `Snr1.chunk0.sub0:0x0063` `c0 01 cc 00 13 c8 00 08 c7`
- `Snr1.chunk0.sub0:0x006c` `c0 02 cc 00 1f c8 00 09 c7`
- `Snr1.chunk0.sub0:0x0075` `c0 02 cc 00 1f c8 00 0a c7`
- `Snr1.chunk0.sub0:0x007e` `c0 02 cc 00 1f c8 00 0b c7`
- `Snr1.chunk0.sub0:0x0087` `c0 01 cc 00 13 c8 00 0c c7`
- `Snr1.chunk0.sub0:0x0090` `c0 01 cc 00 13 c8 00 0d c7`
- `Snr1.chunk0.sub0:0x0099` `c0 01 cc 00 13 c8 00 0e c7`
- `Snr1.chunk0.sub0:0x00a2` `c0 01 cc 00 13 c8 00 0f c7`
- `Snr1.chunk0.sub0:0x00ab` `c0 01 cc 00 13 c8 00 10 c7`
- `Snr1.chunk0.sub0:0x00b4` `c0 01 cc 00 13 c8 00 11 c7`
- `Snr1.chunk0.sub0:0x00d0` `c0 01 cc 00 06 c8 00 12 c7`
- `Snr1.chunk0.sub0:0x00e0` `c0 01 cc 00 06 c8 00 13 c7`
- `Snr1.chunk0.sub0:0x00e9` `c0 02 cc 00 00 c8 00 14 c7`
- `Snr1.chunk0.sub0:0x00f2` `c0 01 cc 00 06 c8 00 15 c7`
- `Snr1.chunk0.sub0:0x0102` `c0 02 cc 00 00 c8 00 16 c7`
- `Snr1.chunk0.sub0:0x010b` `c0 01 cc 00 12 c8 00 17 c7`
- `Snr1.chunk0.sub0:0x0114` `c0 02 cc 00 00 c8 00 18 c7`
- `Snr1.chunk0.sub0:0x011d` `c0 01 cc 00 12 c8 00 19 c7`
- `Snr1.chunk0.sub0:0x0126` `c0 02 cc 00 00 c8 00 1a c7`
- `Snr1.chunk0.sub0:0x012f` `c0 01 cc 00 12 c8 00 1b c7`
- `Snr1.chunk0.sub0:0x0138` `c0 02 cc 00 00 c8 00 1c c7`
- `Snr1.chunk0.sub0:0x0141` `c0 01 cc 00 12 c8 00 1d c7`
- `Snr1.chunk0.sub0:0x014a` `c0 02 cc 00 00 c8 00 1e c7`
- `Snr1.chunk0.sub0:0x0153` `c0 01 cc 00 12 c8 00 1f c7`
- `Snr1.chunk0.sub0:0x015c` `c0 02 cc 00 00 c8 00 20 c7`
- `Snr1.chunk0.sub0:0x0165` `c0 01 cc 00 12 c8 00 21 c7`
- `Snr1.chunk0.sub0:0x016e` `c0 02 cc 00 00 c8 00 22 c7`
- `Snr1.chunk0.sub0:0x0177` `c0 01 cc 00 12 c8 00 23 c7`
- `Snr1.chunk0.sub0:0x0180` `c0 01 cc 00 12 c8 00 24 c7`
- `Snr1.chunk0.sub0:0x0189` `c0 02 cc 00 00 c8 00 25 c7`
- `Snr1.chunk0.sub0:0x0192` `c0 01 cc 00 12 c8 00 26 c7`
- `Snr1.chunk0.sub0:0x019b` `c0 02 cc 00 00 c8 00 27 c7`
