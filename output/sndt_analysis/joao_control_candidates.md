# João Control Candidate Analysis

This removes known long text motifs and short text motifs from `Snr1.chunk0.sub0`, then summarizes the remaining control-looking bytes.

- Code length: `2064`
- Known spans: `87`
- Residual spans: `55`
- Residual bytes: `522`

## Residual Spans

- `0x0000..0x0008` len=8 bytes=`ad 00 01 2a ac 05 00 40`
- `0x0011..0x0024` len=19 bytes=`fe 02 62 ad 05 01 2a ac 01 01 08 0f 01 07 8e 01 42 00 f7`
- `0x00bd..0x00d0` len=19 bytes=`dc 00 06 00 3f 1d 00 34 2c 01 01 fe 02 62 8f 01 41 01 08`
- `0x00d9..0x00e0` len=7 bytes=`fe 02 62 ad 01 01 2a`
- `0x00fb..0x0102` len=7 bytes=`fe 02 62 ac 00 02 62`
- `0x01fe..0x0201` len=3 bytes=`f9 05 05`
- `0x022e..0x0240` len=18 bytes=`fb 45 2c 00 01 fe 02 62 f8 f2 ac 00 02 bf ad 04 02 75`
- `0x0249..0x024d` len=4 bytes=`ac 04 02 be`
- `0x0271..0x0274` len=3 bytes=`c4 ca 04`
- `0x028f..0x02a3` len=20 bytes=`2c 04 01 f8 ad 00 03 cb ad 05 02 d9 ac 01 02 d9 0c 3f 00 01`
- `0x02ac..0x02b5` len=9 bytes=`f8 ac 05 03 cb 0c 3f 00 01`
- `0x0333..0x0339` len=6 bytes=`0c 00 03 e8 e6 00`
- `0x0366..0x0367` len=1 bytes=`c4`
- `0x038b..0x03a4` len=25 bytes=`dc 00 05 00 0f 1d 00 64 dc 00 05 01 0f 1d 00 64 2c 05 01 f8 f2 ac 00 03 d6`
- `0x03aa..0x03ae` len=4 bytes=`ad 00 03 e0`
- `0x03b4..0x03c2` len=14 bytes=`f8 f2 0c 3f 00 01 ac 00 04 20 ad 07 03 f4`
- `0x03c8..0x03cc` len=4 bytes=`ac 07 04 1f`
- `0x03f0..0x03fc` len=12 bytes=`2c 07 01 f8 ad 00 05 5e ad 02 04 8f`
- `0x0402..0x0409` len=7 bytes=`ac 08 04 8f 2c 08 01`
- `0x040f..0x0418` len=9 bytes=`c9 01 00 61 8c 01 00 04 53`
- `0x0421..0x042c` len=11 bytes=`0c 00 03 e8 e6 00 8c 01 01 04 7b`
- `0x0444..0x0454` len=16 bytes=`dc 00 03 00 1c 4c 00 07 1d 00 64 8c 01 02 04 8f`
- `0x0463..0x0467` len=4 bytes=`ac 02 05 5e`
- `0x046d..0x0471` len=4 bytes=`ac 07 04 ac`
- `0x0480..0x0484` len=4 bytes=`ad 07 04 cb`
- `0x04f6..0x04f8` len=2 bytes=`fb 46`
- `0x0513..0x053b` len=40 bytes=`dc 00 0c 62 15 05 01 00 6c 01 20 11 00 01 dc 00 0c 63 15 05 01 00 6c 01 20 11 00 01 2c 02 01 f2 ac 03 05 a3 ac 00 05 7c`
- `0x0550..0x0554` len=4 bytes=`ad 00 05 a2`
- `0x056f..0x0580` len=17 bytes=`fa 05 00 84 2c 03 01 f8 f2 ac 00 05 b8 0c 3f 00 01`
- `0x058c..0x0594` len=8 bytes=`ad 00 07 48 ac 03 05 cc`
- `0x059d..0x05a4` len=7 bytes=`fe 07 48 ac 02 05 f4`
- `0x05aa..0x05ae` len=4 bytes=`ac 07 05 e3`
- `0x05b7..0x05bb` len=4 bytes=`ad 07 05 f0`
- `0x05c4..0x05d4` len=16 bytes=`f8 fe 07 48 ac 01 06 26 ac 05 06 16 ac 08 06 09`
- `0x05dd..0x05e1` len=4 bytes=`ad 08 06 16`
- `0x05ea..0x05ee` len=4 bytes=`ad 05 06 23`
- `0x05f7..0x05fe` len=7 bytes=`fe 07 48 ac 0a 07 48`
- `0x068e..0x069b` len=13 bytes=`dc 0b 03 46 2e 05 0c 0b 8d 0c 04 07 3c`
- `0x06a4..0x06aa` len=6 bytes=`e9 0b ad 0b 07 17`
- `0x06b3..0x06c8` len=21 bytes=`dc 00 03 46 2e 1d 00 04 dc 0b 03 45 2e 05 0c 0b 8d 0c 03 07 05`
- `0x06d1..0x06d9` len=8 bytes=`dc 00 03 45 2e 1d 00 03`
- `0x06eb..0x06ef` len=4 bytes=`ac 0b 07 36`
- `0x070a..0x0710` len=6 bytes=`2c 0a 01 fe 07 48`
- `0x0719..0x0721` len=8 bytes=`2c 0a 01 f2 ac 00 07 66`
- `0x0739..0x0742` len=9 bytes=`f8 ad 00 07 7b ac 03 07 7b`
- `0x074e..0x0758` len=10 bytes=`f8 f2 0c 3f 00 01 ac 00 07 8b`
- `0x075e..0x0767` len=9 bytes=`f8 ad 00 07 c6 ac 09 07 bc`
- `0x0782..0x0794` len=18 bytes=`dc 00 06 00 3f 4c 00 01 1d 00 03 2c 09 01 ad 09 07 c6`
- `0x079a..0x07ac` len=18 bytes=`f2 0c 3f 00 01 ac 00 08 07 eb 00 00 03 8c 00 00 07 e4`
- `0x07b8..0x07bd` len=5 bytes=`8c 00 01 07 f5`
- `0x07c9..0x07ce` len=5 bytes=`8c 00 02 08 06`
- `0x07da..0x07e8` len=14 bytes=`f8 ad 00 08 39 eb 00 00 03 8c 00 00 08 23`
- `0x07f7..0x07fc` len=5 bytes=`8c 00 01 08 2e`
- `0x0802..0x0807` len=5 bytes=`8c 00 02 08 39`
- `0x080d..0x0810` len=3 bytes=`f2 f0 f2`

## Top Residual Bytes

- `00`: 72
- `01`: 45
- `ac`: 30
- `07`: 29
- `05`: 27
- `ad`: 21
- `03`: 21
- `02`: 18
- `04`: 15
- `0c`: 14
- `08`: 12
- `f8`: 12
- `dc`: 11
- `2c`: 11
- `f2`: 10
- `fe`: 9
- `8c`: 9
- `06`: 8
- `3f`: 8
- `62`: 7
- `1d`: 7
- `0b`: 7
- `48`: 6
- `2e`: 5
- `8f`: 4
- `09`: 4
- `2a`: 3
- `0f`: 3
- `45`: 3
- `cb`: 3
- `64`: 3
- `20`: 3

## Target Opcode Contexts

### `ad`

- Count: `21`

Contexts:

- `0x0000` span=0x0000..0x0008 next=`ad 00 01 2a ac 05 00 40` before=None after=Snr1.chunk0.sub0.run0
- `0x0014` span=0x0011..0x0024 next=`ad 05 01 2a ac 01 01 08` before=Snr1.chunk0.sub0.run0 after=Snr1.chunk0.sub0.run1
- `0x00dc` span=0x00d9..0x00e0 next=`ad 01 01 2a c0 01 cc 00` before=Snr1.chunk0.sub0.run2 after=Snr1.chunk0.sub0.run3
- `0x023c` span=0x022e..0x0240 next=`ad 04 02 75 c0 01 cc 00` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x0293` span=0x028f..0x02a3 next=`ad 00 03 cb ad 05 02 d9` before=Snr1.chunk0.sub0.run8 after=Snr1.chunk0.sub0.run9
- `0x0297` span=0x028f..0x02a3 next=`ad 05 02 d9 ac 01 02 d9` before=Snr1.chunk0.sub0.run8 after=Snr1.chunk0.sub0.run9
- `0x03aa` span=0x03aa..0x03ae next=`ad 00 03 e0 c0 00 c8 00` before=Snr1.chunk0.sub0.short44 after=Snr1.chunk0.sub0.short45
- `0x03be` span=0x03b4..0x03c2 next=`ad 07 03 f4 c0 00 c8 00` before=Snr1.chunk0.sub0.short45 after=Snr1.chunk0.sub0.short46
- `0x03f4` span=0x03f0..0x03fc next=`ad 00 05 5e ad 02 04 8f` before=Snr1.chunk0.sub0.run14 after=Snr1.chunk0.sub0.short50
- `0x03f8` span=0x03f0..0x03fc next=`ad 02 04 8f c0 00 c8 00` before=Snr1.chunk0.sub0.run14 after=Snr1.chunk0.sub0.short50
- `0x0480` span=0x0480..0x0484 next=`ad 07 04 cb c0 02 cc 00` before=Snr1.chunk0.sub0.short55 after=Snr1.chunk0.sub0.run19
- `0x0550` span=0x0550..0x0554 next=`ad 00 05 a2 c0 02 cc 00` before=Snr1.chunk0.sub0.short64 after=Snr1.chunk0.sub0.run24
- `0x058c` span=0x058c..0x0594 next=`ad 00 07 48 ac 03 05 cc` before=Snr1.chunk0.sub0.short69 after=Snr1.chunk0.sub0.run25
- `0x05b7` span=0x05b7..0x05bb next=`ad 07 05 f0 c0 02 cc 00` before=Snr1.chunk0.sub0.run26 after=Snr1.chunk0.sub0.run27
- `0x05dd` span=0x05dd..0x05e1 next=`ad 08 06 16 c0 01 cc 00` before=Snr1.chunk0.sub0.run28 after=Snr1.chunk0.sub0.run29
- `0x05ea` span=0x05ea..0x05ee next=`ad 05 06 23 c0 01 cc 00` before=Snr1.chunk0.sub0.run29 after=Snr1.chunk0.sub0.run30
- `0x06a6` span=0x06a4..0x06aa next=`ad 0b 07 17 c0 02 cc 00` before=Snr1.chunk0.sub0.run32 after=Snr1.chunk0.sub0.run33
- `0x073a` span=0x0739..0x0742 next=`ad 00 07 7b ac 03 07 7b` before=Snr1.chunk0.sub0.short74 after=Snr1.chunk0.sub0.short75
- `0x075f` span=0x075e..0x0767 next=`ad 00 07 c6 ac 09 07 bc` before=Snr1.chunk0.sub0.short77 after=Snr1.chunk0.sub0.short78
- `0x0790` span=0x0782..0x0794 next=`ad 09 07 c6 c0 00 c8 00` before=Snr1.chunk0.sub0.short80 after=Snr1.chunk0.sub0.short81
- `0x07db` span=0x07da..0x07e8 next=`ad 00 08 39 eb 00 00 03` before=Snr1.chunk0.sub0.short87 after=Snr1.chunk0.sub0.short88

Top byte forms:

- `len1:ad`: 21
- `len2:ad 00`: 9
- `len2:ad 05`: 3
- `len2:ad 07`: 3
- `len3:ad 00 07`: 3
- `len3:ad 00 03`: 2
- `len3:ad 00 05`: 2
- `len3:ad 00 01`: 1
- `len4:ad 00 01 2a`: 1
- `len5:ad 00 01 2a ac`: 1
- `len3:ad 05 01`: 1
- `len4:ad 05 01 2a`: 1

### `ac`

- Count: `30`

Contexts:

- `0x0004` span=0x0000..0x0008 next=`ac 05 00 40 c0 01 cc 00` before=None after=Snr1.chunk0.sub0.run0
- `0x0018` span=0x0011..0x0024 next=`ac 01 01 08 0f 01 07 8e` before=Snr1.chunk0.sub0.run0 after=Snr1.chunk0.sub0.run1
- `0x00fe` span=0x00fb..0x0102 next=`ac 00 02 62 c0 02 cc 00` before=Snr1.chunk0.sub0.run3 after=Snr1.chunk0.sub0.run4
- `0x0238` span=0x022e..0x0240 next=`ac 00 02 bf ad 04 02 75` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x0249` span=0x0249..0x024d next=`ac 04 02 be c0 01 cc 00` before=Snr1.chunk0.sub0.run6 after=Snr1.chunk0.sub0.run7
- `0x029b` span=0x028f..0x02a3 next=`ac 01 02 d9 0c 3f 00 01` before=Snr1.chunk0.sub0.run8 after=Snr1.chunk0.sub0.run9
- `0x02ad` span=0x02ac..0x02b5 next=`ac 05 03 cb 0c 3f 00 01` before=Snr1.chunk0.sub0.run9 after=Snr1.chunk0.sub0.run10
- `0x03a0` span=0x038b..0x03a4 next=`ac 00 03 d6 c0 00 c8 00` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x03ba` span=0x03b4..0x03c2 next=`ac 00 04 20 ad 07 03 f4` before=Snr1.chunk0.sub0.short45 after=Snr1.chunk0.sub0.short46
- `0x03c8` span=0x03c8..0x03cc next=`ac 07 04 1f c0 00 c8 00` before=Snr1.chunk0.sub0.short46 after=Snr1.chunk0.sub0.short47
- `0x0402` span=0x0402..0x0409 next=`ac 08 04 8f 2c 08 01 c0` before=Snr1.chunk0.sub0.short50 after=Snr1.chunk0.sub0.short51
- `0x0463` span=0x0463..0x0467 next=`ac 02 05 5e c0 00 c8 00` before=Snr1.chunk0.sub0.short53 after=Snr1.chunk0.sub0.short54
- `0x046d` span=0x046d..0x0471 next=`ac 07 04 ac c0 02 cc 00` before=Snr1.chunk0.sub0.short54 after=Snr1.chunk0.sub0.run18
- `0x0470` span=0x046d..0x0471 next=`ac c0 02 cc 00 00 c8 00` before=Snr1.chunk0.sub0.short54 after=Snr1.chunk0.sub0.run18
- `0x0533` span=0x0513..0x053b next=`ac 03 05 a3 ac 00 05 7c` before=Snr1.chunk0.sub0.run22 after=Snr1.chunk0.sub0.short63
- `0x0537` span=0x0513..0x053b next=`ac 00 05 7c c0 00 c8 00` before=Snr1.chunk0.sub0.run22 after=Snr1.chunk0.sub0.short63
- `0x0578` span=0x056f..0x0580 next=`ac 00 05 b8 0c 3f 00 01` before=Snr1.chunk0.sub0.short67 after=Snr1.chunk0.sub0.short68
- `0x0590` span=0x058c..0x0594 next=`ac 03 05 cc c0 01 cc 00` before=Snr1.chunk0.sub0.short69 after=Snr1.chunk0.sub0.run25
- `0x05a0` span=0x059d..0x05a4 next=`ac 02 05 f4 c0 00 c8 00` before=Snr1.chunk0.sub0.run25 after=Snr1.chunk0.sub0.short70
- `0x05aa` span=0x05aa..0x05ae next=`ac 07 05 e3 c0 02 cc 00` before=Snr1.chunk0.sub0.short70 after=Snr1.chunk0.sub0.run26
- `0x05c8` span=0x05c4..0x05d4 next=`ac 01 06 26 ac 05 06 16` before=Snr1.chunk0.sub0.run27 after=Snr1.chunk0.sub0.run28
- `0x05cc` span=0x05c4..0x05d4 next=`ac 05 06 16 ac 08 06 09` before=Snr1.chunk0.sub0.run27 after=Snr1.chunk0.sub0.run28
- `0x05d0` span=0x05c4..0x05d4 next=`ac 08 06 09 c0 01 cc 00` before=Snr1.chunk0.sub0.run27 after=Snr1.chunk0.sub0.run28
- `0x05fa` span=0x05f7..0x05fe next=`ac 0a 07 48 c0 01 cc 00` before=Snr1.chunk0.sub0.run30 after=Snr1.chunk0.sub0.run31
- `0x06eb` span=0x06eb..0x06ef next=`ac 0b 07 36 c0 02 cc 00` before=Snr1.chunk0.sub0.run35 after=Snr1.chunk0.sub0.run36
- `0x071d` span=0x0719..0x0721 next=`ac 00 07 66 c0 00 c8 00` before=Snr1.chunk0.sub0.run37 after=Snr1.chunk0.sub0.short71
- `0x073e` span=0x0739..0x0742 next=`ac 03 07 7b c0 00 c8 00` before=Snr1.chunk0.sub0.short74 after=Snr1.chunk0.sub0.short75
- `0x0754` span=0x074e..0x0758 next=`ac 00 07 8b c0 00 c8 00` before=Snr1.chunk0.sub0.short76 after=Snr1.chunk0.sub0.short77
- `0x0763` span=0x075e..0x0767 next=`ac 09 07 bc c0 00 c8 00` before=Snr1.chunk0.sub0.short77 after=Snr1.chunk0.sub0.short78
- `0x079f` span=0x079a..0x07ac next=`ac 00 08 07 eb 00 00 03` before=Snr1.chunk0.sub0.short81 after=Snr1.chunk0.sub0.short82

Top byte forms:

- `len1:ac`: 30
- `len2:ac 00`: 9
- `len2:ac 05`: 3
- `len2:ac 01`: 3
- `len2:ac 07`: 3
- `len2:ac 03`: 3
- `len3:ac 00 02`: 2
- `len3:ac 07 04`: 2
- `len2:ac 08`: 2
- `len2:ac 02`: 2
- `len3:ac 02 05`: 2
- `len3:ac 03 05`: 2

### `fe`

- Count: `9`

Contexts:

- `0x0011` span=0x0011..0x0024 next=`fe 02 62 ad 05 01 2a ac` before=Snr1.chunk0.sub0.run0 after=Snr1.chunk0.sub0.run1
- `0x00c8` span=0x00bd..0x00d0 next=`fe 02 62 8f 01 41 01 08` before=Snr1.chunk0.sub0.run1 after=Snr1.chunk0.sub0.run2
- `0x00d9` span=0x00d9..0x00e0 next=`fe 02 62 ad 01 01 2a c0` before=Snr1.chunk0.sub0.run2 after=Snr1.chunk0.sub0.run3
- `0x00fb` span=0x00fb..0x0102 next=`fe 02 62 ac 00 02 62 c0` before=Snr1.chunk0.sub0.run3 after=Snr1.chunk0.sub0.run4
- `0x0233` span=0x022e..0x0240 next=`fe 02 62 f8 f2 ac 00 02` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x059d` span=0x059d..0x05a4 next=`fe 07 48 ac 02 05 f4 c0` before=Snr1.chunk0.sub0.run25 after=Snr1.chunk0.sub0.short70
- `0x05c5` span=0x05c4..0x05d4 next=`fe 07 48 ac 01 06 26 ac` before=Snr1.chunk0.sub0.run27 after=Snr1.chunk0.sub0.run28
- `0x05f7` span=0x05f7..0x05fe next=`fe 07 48 ac 0a 07 48 c0` before=Snr1.chunk0.sub0.run30 after=Snr1.chunk0.sub0.run31
- `0x070d` span=0x070a..0x0710 next=`fe 07 48 c0 01 cc 00 1f` before=Snr1.chunk0.sub0.run36 after=Snr1.chunk0.sub0.run37

Top byte forms:

- `len1:fe`: 9
- `len2:fe 02`: 5
- `len3:fe 02 62`: 5
- `len2:fe 07`: 4
- `len3:fe 07 48`: 4
- `len4:fe 07 48 ac`: 3
- `len4:fe 02 62 ad`: 2
- `len5:fe 02 62 ad 05`: 1
- `len4:fe 02 62 8f`: 1
- `len5:fe 02 62 8f 01`: 1
- `len5:fe 02 62 ad 01`: 1
- `len4:fe 02 62 ac`: 1

### `f8`

- Count: `12`

Contexts:

- `0x0236` span=0x022e..0x0240 next=`f8 f2 ac 00 02 bf ad 04` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x0292` span=0x028f..0x02a3 next=`f8 ad 00 03 cb ad 05 02` before=Snr1.chunk0.sub0.run8 after=Snr1.chunk0.sub0.run9
- `0x02ac` span=0x02ac..0x02b5 next=`f8 ac 05 03 cb 0c 3f 00` before=Snr1.chunk0.sub0.run9 after=Snr1.chunk0.sub0.run10
- `0x039e` span=0x038b..0x03a4 next=`f8 f2 ac 00 03 d6 c0 00` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x03b4` span=0x03b4..0x03c2 next=`f8 f2 0c 3f 00 01 ac 00` before=Snr1.chunk0.sub0.short45 after=Snr1.chunk0.sub0.short46
- `0x03f3` span=0x03f0..0x03fc next=`f8 ad 00 05 5e ad 02 04` before=Snr1.chunk0.sub0.run14 after=Snr1.chunk0.sub0.short50
- `0x0576` span=0x056f..0x0580 next=`f8 f2 ac 00 05 b8 0c 3f` before=Snr1.chunk0.sub0.short67 after=Snr1.chunk0.sub0.short68
- `0x05c4` span=0x05c4..0x05d4 next=`f8 fe 07 48 ac 01 06 26` before=Snr1.chunk0.sub0.run27 after=Snr1.chunk0.sub0.run28
- `0x0739` span=0x0739..0x0742 next=`f8 ad 00 07 7b ac 03 07` before=Snr1.chunk0.sub0.short74 after=Snr1.chunk0.sub0.short75
- `0x074e` span=0x074e..0x0758 next=`f8 f2 0c 3f 00 01 ac 00` before=Snr1.chunk0.sub0.short76 after=Snr1.chunk0.sub0.short77
- `0x075e` span=0x075e..0x0767 next=`f8 ad 00 07 c6 ac 09 07` before=Snr1.chunk0.sub0.short77 after=Snr1.chunk0.sub0.short78
- `0x07da` span=0x07da..0x07e8 next=`f8 ad 00 08 39 eb 00 00` before=Snr1.chunk0.sub0.short87 after=Snr1.chunk0.sub0.short88

Top byte forms:

- `len1:f8`: 12
- `len2:f8 f2`: 5
- `len2:f8 ad`: 5
- `len3:f8 ad 00`: 5
- `len3:f8 f2 ac`: 3
- `len4:f8 f2 ac 00`: 3
- `len3:f8 f2 0c`: 2
- `len4:f8 f2 0c 3f`: 2
- `len5:f8 f2 0c 3f 00`: 2
- `len4:f8 ad 00 07`: 2
- `len5:f8 f2 ac 00 02`: 1
- `len4:f8 ad 00 03`: 1

### `f9`

- Count: `1`

Contexts:

- `0x01fe` span=0x01fe..0x0201 next=`f9 05 05 c0 01 cc 00 12` before=Snr1.chunk0.sub0.run4 after=Snr1.chunk0.sub0.run5

Top byte forms:

- `len1:f9`: 1
- `len2:f9 05`: 1
- `len3:f9 05 05`: 1
- `len4:f9 05 05 c0`: 1
- `len5:f9 05 05 c0 01`: 1

### `fb`

- Count: `2`

Contexts:

- `0x022e` span=0x022e..0x0240 next=`fb 45 2c 00 01 fe 02 62` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x04f6` span=0x04f6..0x04f8 next=`fb 46 c0 02 cc 00 1f c8` before=Snr1.chunk0.sub0.run21 after=Snr1.chunk0.sub0.run22

Top byte forms:

- `len1:fb`: 2
- `len2:fb 45`: 1
- `len3:fb 45 2c`: 1
- `len4:fb 45 2c 00`: 1
- `len5:fb 45 2c 00 01`: 1
- `len2:fb 46`: 1
- `len3:fb 46 c0`: 1
- `len4:fb 46 c0 02`: 1
- `len5:fb 46 c0 02 cc`: 1

### `dc`

- Count: `11`

Contexts:

- `0x00bd` span=0x00bd..0x00d0 next=`dc 00 06 00 3f 1d 00 34` before=Snr1.chunk0.sub0.run1 after=Snr1.chunk0.sub0.run2
- `0x038b` span=0x038b..0x03a4 next=`dc 00 05 00 0f 1d 00 64` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x0393` span=0x038b..0x03a4 next=`dc 00 05 01 0f 1d 00 64` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x0444` span=0x0444..0x0454 next=`dc 00 03 00 1c 4c 00 07` before=Snr1.chunk0.sub0.short52 after=Snr1.chunk0.sub0.run17
- `0x0513` span=0x0513..0x053b next=`dc 00 0c 62 15 05 01 00` before=Snr1.chunk0.sub0.run22 after=Snr1.chunk0.sub0.short63
- `0x0521` span=0x0513..0x053b next=`dc 00 0c 63 15 05 01 00` before=Snr1.chunk0.sub0.run22 after=Snr1.chunk0.sub0.short63
- `0x068e` span=0x068e..0x069b next=`dc 0b 03 46 2e 05 0c 0b` before=Snr1.chunk0.sub0.run31 after=Snr1.chunk0.sub0.run32
- `0x06b3` span=0x06b3..0x06c8 next=`dc 00 03 46 2e 1d 00 04` before=Snr1.chunk0.sub0.run33 after=Snr1.chunk0.sub0.run34
- `0x06bb` span=0x06b3..0x06c8 next=`dc 0b 03 45 2e 05 0c 0b` before=Snr1.chunk0.sub0.run33 after=Snr1.chunk0.sub0.run34
- `0x06d1` span=0x06d1..0x06d9 next=`dc 00 03 45 2e 1d 00 03` before=Snr1.chunk0.sub0.run34 after=Snr1.chunk0.sub0.run35
- `0x0782` span=0x0782..0x0794 next=`dc 00 06 00 3f 4c 00 01` before=Snr1.chunk0.sub0.short80 after=Snr1.chunk0.sub0.short81

Top byte forms:

- `len1:dc`: 11
- `len2:dc 00`: 9
- `len3:dc 00 03`: 3
- `len3:dc 00 06`: 2
- `len4:dc 00 06 00`: 2
- `len5:dc 00 06 00 3f`: 2
- `len3:dc 00 05`: 2
- `len3:dc 00 0c`: 2
- `len2:dc 0b`: 2
- `len3:dc 0b 03`: 2
- `len4:dc 00 05 00`: 1
- `len5:dc 00 05 00 0f`: 1

### `8c`

- Count: `9`

Contexts:

- `0x0413` span=0x040f..0x0418 next=`8c 01 00 04 53 c0 02 cc` before=Snr1.chunk0.sub0.short51 after=Snr1.chunk0.sub0.run15
- `0x0427` span=0x0421..0x042c next=`8c 01 01 04 7b c0 02 cc` before=Snr1.chunk0.sub0.run15 after=Snr1.chunk0.sub0.run16
- `0x044f` span=0x0444..0x0454 next=`8c 01 02 04 8f c0 02 cc` before=Snr1.chunk0.sub0.short52 after=Snr1.chunk0.sub0.run17
- `0x07a7` span=0x079a..0x07ac next=`8c 00 00 07 e4 c0 00 c8` before=Snr1.chunk0.sub0.short81 after=Snr1.chunk0.sub0.short82
- `0x07b8` span=0x07b8..0x07bd next=`8c 00 01 07 f5 c0 00 c8` before=Snr1.chunk0.sub0.short83 after=Snr1.chunk0.sub0.short84
- `0x07c9` span=0x07c9..0x07ce next=`8c 00 02 08 06 c0 00 c8` before=Snr1.chunk0.sub0.short85 after=Snr1.chunk0.sub0.short86
- `0x07e3` span=0x07da..0x07e8 next=`8c 00 00 08 23 c0 00 c8` before=Snr1.chunk0.sub0.short87 after=Snr1.chunk0.sub0.short88
- `0x07f7` span=0x07f7..0x07fc next=`8c 00 01 08 2e c0 00 c8` before=Snr1.chunk0.sub0.run39 after=Snr1.chunk0.sub0.short89
- `0x0802` span=0x0802..0x0807 next=`8c 00 02 08 39 c0 00 c8` before=Snr1.chunk0.sub0.short89 after=Snr1.chunk0.sub0.short90

Top byte forms:

- `len1:8c`: 9
- `len2:8c 00`: 6
- `len2:8c 01`: 3
- `len3:8c 00 00`: 2
- `len3:8c 00 01`: 2
- `len3:8c 00 02`: 2
- `len4:8c 00 02 08`: 2
- `len3:8c 01 00`: 1
- `len4:8c 01 00 04`: 1
- `len5:8c 01 00 04 53`: 1
- `len3:8c 01 01`: 1
- `len4:8c 01 01 04`: 1

### `8f`

- Count: `4`

Contexts:

- `0x00cb` span=0x00bd..0x00d0 next=`8f 01 41 01 08 c0 01 cc` before=Snr1.chunk0.sub0.run1 after=Snr1.chunk0.sub0.run2
- `0x03fb` span=0x03f0..0x03fc next=`8f c0 00 c8 00 5f c7 ac` before=Snr1.chunk0.sub0.run14 after=Snr1.chunk0.sub0.short50
- `0x0405` span=0x0402..0x0409 next=`8f 2c 08 01 c0 00 c8 00` before=Snr1.chunk0.sub0.short50 after=Snr1.chunk0.sub0.short51
- `0x0453` span=0x0444..0x0454 next=`8f c0 02 cc 00 00 c8 00` before=Snr1.chunk0.sub0.short52 after=Snr1.chunk0.sub0.run17

Top byte forms:

- `len1:8f`: 4
- `len2:8f c0`: 2
- `len2:8f 01`: 1
- `len3:8f 01 41`: 1
- `len4:8f 01 41 01`: 1
- `len5:8f 01 41 01 08`: 1
- `len3:8f c0 00`: 1
- `len4:8f c0 00 c8`: 1
- `len5:8f c0 00 c8 00`: 1
- `len2:8f 2c`: 1
- `len3:8f 2c 08`: 1
- `len4:8f 2c 08 01`: 1

### `0f`

- Count: `3`

Contexts:

- `0x001c` span=0x0011..0x0024 next=`0f 01 07 8e 01 42 00 f7` before=Snr1.chunk0.sub0.run0 after=Snr1.chunk0.sub0.run1
- `0x038f` span=0x038b..0x03a4 next=`0f 1d 00 64 dc 00 05 01` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x0397` span=0x038b..0x03a4 next=`0f 1d 00 64 2c 05 01 f8` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44

Top byte forms:

- `len1:0f`: 3
- `len2:0f 1d`: 2
- `len3:0f 1d 00`: 2
- `len4:0f 1d 00 64`: 2
- `len2:0f 01`: 1
- `len3:0f 01 07`: 1
- `len4:0f 01 07 8e`: 1
- `len5:0f 01 07 8e 01`: 1
- `len5:0f 1d 00 64 dc`: 1
- `len5:0f 1d 00 64 2c`: 1

### `1d`

- Count: `7`

Contexts:

- `0x00c2` span=0x00bd..0x00d0 next=`1d 00 34 2c 01 01 fe 02` before=Snr1.chunk0.sub0.run1 after=Snr1.chunk0.sub0.run2
- `0x0390` span=0x038b..0x03a4 next=`1d 00 64 dc 00 05 01 0f` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x0398` span=0x038b..0x03a4 next=`1d 00 64 2c 05 01 f8 f2` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x044c` span=0x0444..0x0454 next=`1d 00 64 8c 01 02 04 8f` before=Snr1.chunk0.sub0.short52 after=Snr1.chunk0.sub0.run17
- `0x06b8` span=0x06b3..0x06c8 next=`1d 00 04 dc 0b 03 45 2e` before=Snr1.chunk0.sub0.run33 after=Snr1.chunk0.sub0.run34
- `0x06d6` span=0x06d1..0x06d9 next=`1d 00 03 c0 01 cc 00 20` before=Snr1.chunk0.sub0.run34 after=Snr1.chunk0.sub0.run35
- `0x078a` span=0x0782..0x0794 next=`1d 00 03 2c 09 01 ad 09` before=Snr1.chunk0.sub0.short80 after=Snr1.chunk0.sub0.short81

Top byte forms:

- `len1:1d`: 7
- `len2:1d 00`: 7
- `len3:1d 00 64`: 3
- `len3:1d 00 03`: 2
- `len3:1d 00 34`: 1
- `len4:1d 00 34 2c`: 1
- `len5:1d 00 34 2c 01`: 1
- `len4:1d 00 64 dc`: 1
- `len5:1d 00 64 dc 00`: 1
- `len4:1d 00 64 2c`: 1
- `len5:1d 00 64 2c 05`: 1
- `len4:1d 00 64 8c`: 1

### `2c`

- Count: `11`

Contexts:

- `0x00c5` span=0x00bd..0x00d0 next=`2c 01 01 fe 02 62 8f 01` before=Snr1.chunk0.sub0.run1 after=Snr1.chunk0.sub0.run2
- `0x0230` span=0x022e..0x0240 next=`2c 00 01 fe 02 62 f8 f2` before=Snr1.chunk0.sub0.run5 after=Snr1.chunk0.sub0.run6
- `0x028f` span=0x028f..0x02a3 next=`2c 04 01 f8 ad 00 03 cb` before=Snr1.chunk0.sub0.run8 after=Snr1.chunk0.sub0.run9
- `0x039b` span=0x038b..0x03a4 next=`2c 05 01 f8 f2 ac 00 03` before=Snr1.chunk0.sub0.run12 after=Snr1.chunk0.sub0.short44
- `0x03f0` span=0x03f0..0x03fc next=`2c 07 01 f8 ad 00 05 5e` before=Snr1.chunk0.sub0.run14 after=Snr1.chunk0.sub0.short50
- `0x0406` span=0x0402..0x0409 next=`2c 08 01 c0 00 c8 00 60` before=Snr1.chunk0.sub0.short50 after=Snr1.chunk0.sub0.short51
- `0x052f` span=0x0513..0x053b next=`2c 02 01 f2 ac 03 05 a3` before=Snr1.chunk0.sub0.run22 after=Snr1.chunk0.sub0.short63
- `0x0573` span=0x056f..0x0580 next=`2c 03 01 f8 f2 ac 00 05` before=Snr1.chunk0.sub0.short67 after=Snr1.chunk0.sub0.short68
- `0x070a` span=0x070a..0x0710 next=`2c 0a 01 fe 07 48 c0 01` before=Snr1.chunk0.sub0.run36 after=Snr1.chunk0.sub0.run37
- `0x0719` span=0x0719..0x0721 next=`2c 0a 01 f2 ac 00 07 66` before=Snr1.chunk0.sub0.run37 after=Snr1.chunk0.sub0.short71
- `0x078d` span=0x0782..0x0794 next=`2c 09 01 ad 09 07 c6 c0` before=Snr1.chunk0.sub0.short80 after=Snr1.chunk0.sub0.short81

Top byte forms:

- `len1:2c`: 11
- `len2:2c 0a`: 2
- `len3:2c 0a 01`: 2
- `len2:2c 01`: 1
- `len3:2c 01 01`: 1
- `len4:2c 01 01 fe`: 1
- `len5:2c 01 01 fe 02`: 1
- `len2:2c 00`: 1
- `len3:2c 00 01`: 1
- `len4:2c 00 01 fe`: 1
- `len5:2c 00 01 fe 02`: 1
- `len2:2c 04`: 1

## Initial Interpretation

- After removing long and short text motifs, residual bytes drop to the control layer around the text timeline.
- `ad` and `ac` mostly appear as 4-byte-looking forms near segment boundaries, for example `ad 00 01 2a` and `ac 05 00 40`.
- `fe 02 62` and `fe 07 48` look like compact control separators or calls with a 2-byte operand.
- `f8` often appears immediately before `f2`, `ad`, or `fe`, so it is a high-priority branch/return modifier candidate.
- The next disassembler pass should treat these as candidate lengths only, then test whether residual spans align cleanly.
