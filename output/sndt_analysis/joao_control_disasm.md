# João Control Layer Prototype Disassembly

Prototype disassembly over residual bytes after long and short text motifs are removed.
This tests candidate lengths only; names and semantics are not confirmed.

- Residual bytes: `522`
- Instructions: `195`
- Unknown bytes: `43`

## Opcode Counts

- `ac_control`: 29
- `ad_control`: 21
- `f8_prefix_or_branch`: 12
- `2c_control`: 11
- `dc_control`: 11
- `end_subscript`: 10
- `show_text_byte`: 10
- `8c_control`: 9
- `db_00`: 9
- `db_01`: 9
- `fe_control`: 9
- `2e_control`: 4
- `0f_control`: 3
- `1d_control`: 3
- `db_03`: 3
- `11_control`: 2
- `15_control`: 2
- `4c_control`: 2
- `8d_control`: 2
- `db_04`: 2
- `db_07`: 2
- `db_20`: 2
- `db_3f`: 2
- `db_64`: 2
- `db_c4`: 2
- `db_e8`: 2
- `e6_control`: 2
- `eb_control`: 2
- `fb_control`: 2
- `8f_control`: 1
- `c9_control`: 1
- `db_05`: 1
- `db_08`: 1
- `db_1c`: 1
- `db_3c`: 1
- `db_42`: 1
- `db_8e`: 1
- `db_ca`: 1
- `db_f7`: 1
- `e9_control`: 1
- `f0_control`: 1
- `f9_control`: 1
- `fa_control`: 1

## Spans

### 0x0000..0x0008

- Length: `8`
- Unknown bytes: `0`

```text
0x0000: ad 00 01 2a    ad_control 298
0x0004: ac 05 00 40    ac_control 327744
```

### 0x0011..0x0024

- Length: `19`
- Unknown bytes: `5`

```text
0x0011: fe 02 62       fe_control 610
0x0014: ad 05 01 2a    ad_control 327978
0x0018: ac 01 01 08    ac_control 65800
0x001c: 0f 01 07       0f_control 263
0x001f: 8e             db_8e
0x0020: 01             db_01
0x0021: 42             db_42
0x0022: 00             db_00
0x0023: f7             db_f7
```

### 0x00bd..0x00d0

- Length: `19`
- Unknown bytes: `2`

```text
0x00bd: dc 00 06 00    dc_control 1536
0x00c1: 3f             db_3f
0x00c2: 1d 00 34       1d_control 52
0x00c5: 2c 01 01       2c_control 257
0x00c8: fe 02 62       fe_control 610
0x00cb: 8f 01 41 01    8f_control 82177
0x00cf: 08             db_08
```

### 0x00d9..0x00e0

- Length: `7`
- Unknown bytes: `0`

```text
0x00d9: fe 02 62       fe_control 610
0x00dc: ad 01 01 2a    ad_control 65834
```

### 0x00fb..0x0102

- Length: `7`
- Unknown bytes: `0`

```text
0x00fb: fe 02 62       fe_control 610
0x00fe: ac 00 02 62    ac_control 610
```

### 0x01fe..0x0201

- Length: `3`
- Unknown bytes: `0`

```text
0x01fe: f9 05 05       f9_control 1285
```

### 0x022e..0x0240

- Length: `18`
- Unknown bytes: `0`

```text
0x022e: fb 45          fb_control 69
0x0230: 2c 00 01       2c_control 1
0x0233: fe 02 62       fe_control 610
0x0236: f8             f8_prefix_or_branch
0x0237: f2             end_subscript
0x0238: ac 00 02 bf    ac_control 703
0x023c: ad 04 02 75    ad_control 262773
```

### 0x0249..0x024d

- Length: `4`
- Unknown bytes: `0`

```text
0x0249: ac 04 02 be    ac_control 262846
```

### 0x0271..0x0274

- Length: `3`
- Unknown bytes: `3`

```text
0x0271: c4             db_c4
0x0272: ca             db_ca
0x0273: 04             db_04
```

### 0x028f..0x02a3

- Length: `20`
- Unknown bytes: `2`

```text
0x028f: 2c 04 01       2c_control 1025
0x0292: f8             f8_prefix_or_branch
0x0293: ad 00 03 cb    ad_control 971
0x0297: ad 05 02 d9    ad_control 328409
0x029b: ac 01 02 d9    ac_control 66265
0x029f: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x02a1: 00             db_00
0x02a2: 01             db_01
```

### 0x02ac..0x02b5

- Length: `9`
- Unknown bytes: `2`

```text
0x02ac: f8             f8_prefix_or_branch
0x02ad: ac 05 03 cb    ac_control 328651
0x02b1: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x02b3: 00             db_00
0x02b4: 01             db_01
```

### 0x0333..0x0339

- Length: `6`
- Unknown bytes: `2`

```text
0x0333: 0c 00          show_text_byte 0 ; 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
0x0335: 03             db_03
0x0336: e8             db_e8
0x0337: e6 00          e6_control 0
```

### 0x0366..0x0367

- Length: `1`
- Unknown bytes: `1`

```text
0x0366: c4             db_c4
```

### 0x038b..0x03a4

- Length: `25`
- Unknown bytes: `2`

```text
0x038b: dc 00 05 00    dc_control 1280
0x038f: 0f 1d 00       0f_control 7424
0x0392: 64             db_64
0x0393: dc 00 05 01    dc_control 1281
0x0397: 0f 1d 00       0f_control 7424
0x039a: 64             db_64
0x039b: 2c 05 01       2c_control 1281
0x039e: f8             f8_prefix_or_branch
0x039f: f2             end_subscript
0x03a0: ac 00 03 d6    ac_control 982
```

### 0x03aa..0x03ae

- Length: `4`
- Unknown bytes: `0`

```text
0x03aa: ad 00 03 e0    ad_control 992
```

### 0x03b4..0x03c2

- Length: `14`
- Unknown bytes: `2`

```text
0x03b4: f8             f8_prefix_or_branch
0x03b5: f2             end_subscript
0x03b6: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x03b8: 00             db_00
0x03b9: 01             db_01
0x03ba: ac 00 04 20    ac_control 1056
0x03be: ad 07 03 f4    ad_control 459764
```

### 0x03c8..0x03cc

- Length: `4`
- Unknown bytes: `0`

```text
0x03c8: ac 07 04 1f    ac_control 459807
```

### 0x03f0..0x03fc

- Length: `12`
- Unknown bytes: `0`

```text
0x03f0: 2c 07 01       2c_control 1793
0x03f3: f8             f8_prefix_or_branch
0x03f4: ad 00 05 5e    ad_control 1374
0x03f8: ad 02 04 8f    ad_control 132239
```

### 0x0402..0x0409

- Length: `7`
- Unknown bytes: `0`

```text
0x0402: ac 08 04 8f    ac_control 525455
0x0406: 2c 08 01       2c_control 2049
```

### 0x040f..0x0418

- Length: `9`
- Unknown bytes: `0`

```text
0x040f: c9 01 00 61    c9_control 65633
0x0413: 8c 01 00 04 53 8c_control 16778323
```

### 0x0421..0x042c

- Length: `11`
- Unknown bytes: `2`

```text
0x0421: 0c 00          show_text_byte 0 ; 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
0x0423: 03             db_03
0x0424: e8             db_e8
0x0425: e6 00          e6_control 0
0x0427: 8c 01 01 04 7b 8c_control 16843899
```

### 0x0444..0x0454

- Length: `16`
- Unknown bytes: `1`

```text
0x0444: dc 00 03 00    dc_control 768
0x0448: 1c             db_1c
0x0449: 4c 00 07       4c_control 7
0x044c: 1d 00 64       1d_control 100
0x044f: 8c 01 02 04 8f 8c_control 16909455
```

### 0x0463..0x0467

- Length: `4`
- Unknown bytes: `0`

```text
0x0463: ac 02 05 5e    ac_control 132446
```

### 0x046d..0x0471

- Length: `4`
- Unknown bytes: `0`

```text
0x046d: ac 07 04 ac    ac_control 459948
```

### 0x0480..0x0484

- Length: `4`
- Unknown bytes: `0`

```text
0x0480: ad 07 04 cb    ad_control 459979
```

### 0x04f6..0x04f8

- Length: `2`
- Unknown bytes: `0`

```text
0x04f6: fb 46          fb_control 70
```

### 0x0513..0x053b

- Length: `40`
- Unknown bytes: `4`

```text
0x0513: dc 00 0c 62    dc_control 3170
0x0517: 15 05 01 00 6c 15_control 83951724
0x051c: 01             db_01
0x051d: 20             db_20
0x051e: 11 00 01       11_control 1
0x0521: dc 00 0c 63    dc_control 3171
0x0525: 15 05 01 00 6c 15_control 83951724
0x052a: 01             db_01
0x052b: 20             db_20
0x052c: 11 00 01       11_control 1
0x052f: 2c 02 01       2c_control 513
0x0532: f2             end_subscript
0x0533: ac 03 05 a3    ac_control 198051
0x0537: ac 00 05 7c    ac_control 1404
```

### 0x0550..0x0554

- Length: `4`
- Unknown bytes: `0`

```text
0x0550: ad 00 05 a2    ad_control 1442
```

### 0x056f..0x0580

- Length: `17`
- Unknown bytes: `2`

```text
0x056f: fa 05 00 84    fa_control 327812
0x0573: 2c 03 01       2c_control 769
0x0576: f8             f8_prefix_or_branch
0x0577: f2             end_subscript
0x0578: ac 00 05 b8    ac_control 1464
0x057c: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x057e: 00             db_00
0x057f: 01             db_01
```

### 0x058c..0x0594

- Length: `8`
- Unknown bytes: `0`

```text
0x058c: ad 00 07 48    ad_control 1864
0x0590: ac 03 05 cc    ac_control 198092
```

### 0x059d..0x05a4

- Length: `7`
- Unknown bytes: `0`

```text
0x059d: fe 07 48       fe_control 1864
0x05a0: ac 02 05 f4    ac_control 132596
```

### 0x05aa..0x05ae

- Length: `4`
- Unknown bytes: `0`

```text
0x05aa: ac 07 05 e3    ac_control 460259
```

### 0x05b7..0x05bb

- Length: `4`
- Unknown bytes: `0`

```text
0x05b7: ad 07 05 f0    ad_control 460272
```

### 0x05c4..0x05d4

- Length: `16`
- Unknown bytes: `0`

```text
0x05c4: f8             f8_prefix_or_branch
0x05c5: fe 07 48       fe_control 1864
0x05c8: ac 01 06 26    ac_control 67110
0x05cc: ac 05 06 16    ac_control 329238
0x05d0: ac 08 06 09    ac_control 525833
```

### 0x05dd..0x05e1

- Length: `4`
- Unknown bytes: `0`

```text
0x05dd: ad 08 06 16    ad_control 525846
```

### 0x05ea..0x05ee

- Length: `4`
- Unknown bytes: `0`

```text
0x05ea: ad 05 06 23    ad_control 329251
```

### 0x05f7..0x05fe

- Length: `7`
- Unknown bytes: `0`

```text
0x05f7: fe 07 48       fe_control 1864
0x05fa: ac 0a 07 48    ac_control 657224
```

### 0x068e..0x069b

- Length: `13`
- Unknown bytes: `2`

```text
0x068e: dc 0b 03 46    dc_control 721734
0x0692: 2e 05          2e_control 5
0x0694: 0c 0b          show_text_byte 11 ; 因為沒有比航海更能鍛練男子漢的．
0x0696: 8d 0c 04       8d_control 3076
0x0699: 07             db_07
0x069a: 3c             db_3c
```

### 0x06a4..0x06aa

- Length: `6`
- Unknown bytes: `0`

```text
0x06a4: e9 0b          e9_control 11
0x06a6: ad 0b 07 17    ad_control 722711
```

### 0x06b3..0x06c8

- Length: `21`
- Unknown bytes: `4`

```text
0x06b3: dc 00 03 46    dc_control 838
0x06b7: 2e 1d          2e_control 29
0x06b9: 00             db_00
0x06ba: 04             db_04
0x06bb: dc 0b 03 45    dc_control 721733
0x06bf: 2e 05          2e_control 5
0x06c1: 0c 0b          show_text_byte 11 ; 因為沒有比航海更能鍛練男子漢的．
0x06c3: 8d 0c 03       8d_control 3075
0x06c6: 07             db_07
0x06c7: 05             db_05
```

### 0x06d1..0x06d9

- Length: `8`
- Unknown bytes: `2`

```text
0x06d1: dc 00 03 45    dc_control 837
0x06d5: 2e 1d          2e_control 29
0x06d7: 00             db_00
0x06d8: 03             db_03
```

### 0x06eb..0x06ef

- Length: `4`
- Unknown bytes: `0`

```text
0x06eb: ac 0b 07 36    ac_control 722742
```

### 0x070a..0x0710

- Length: `6`
- Unknown bytes: `0`

```text
0x070a: 2c 0a 01       2c_control 2561
0x070d: fe 07 48       fe_control 1864
```

### 0x0719..0x0721

- Length: `8`
- Unknown bytes: `0`

```text
0x0719: 2c 0a 01       2c_control 2561
0x071c: f2             end_subscript
0x071d: ac 00 07 66    ac_control 1894
```

### 0x0739..0x0742

- Length: `9`
- Unknown bytes: `0`

```text
0x0739: f8             f8_prefix_or_branch
0x073a: ad 00 07 7b    ad_control 1915
0x073e: ac 03 07 7b    ac_control 198523
```

### 0x074e..0x0758

- Length: `10`
- Unknown bytes: `2`

```text
0x074e: f8             f8_prefix_or_branch
0x074f: f2             end_subscript
0x0750: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x0752: 00             db_00
0x0753: 01             db_01
0x0754: ac 00 07 8b    ac_control 1931
```

### 0x075e..0x0767

- Length: `9`
- Unknown bytes: `0`

```text
0x075e: f8             f8_prefix_or_branch
0x075f: ad 00 07 c6    ad_control 1990
0x0763: ac 09 07 bc    ac_control 591804
```

### 0x0782..0x0794

- Length: `18`
- Unknown bytes: `1`

```text
0x0782: dc 00 06 00    dc_control 1536
0x0786: 3f             db_3f
0x0787: 4c 00 01       4c_control 1
0x078a: 1d 00 03       1d_control 3
0x078d: 2c 09 01       2c_control 2305
0x0790: ad 09 07 c6    ad_control 591814
```

### 0x079a..0x07ac

- Length: `18`
- Unknown bytes: `2`

```text
0x079a: f2             end_subscript
0x079b: 0c 3f          show_text_byte 63 ; 太太要您晚上10點到12點之間去公爵府．
0x079d: 00             db_00
0x079e: 01             db_01
0x079f: ac 00 08 07    ac_control 2055
0x07a3: eb 00 00 03    eb_control 3
0x07a7: 8c 00 00 07 e4 8c_control 2020
```

### 0x07b8..0x07bd

- Length: `5`
- Unknown bytes: `0`

```text
0x07b8: 8c 00 01 07 f5 8c_control 67573
```

### 0x07c9..0x07ce

- Length: `5`
- Unknown bytes: `0`

```text
0x07c9: 8c 00 02 08 06 8c_control 133126
```

### 0x07da..0x07e8

- Length: `14`
- Unknown bytes: `0`

```text
0x07da: f8             f8_prefix_or_branch
0x07db: ad 00 08 39    ad_control 2105
0x07df: eb 00 00 03    eb_control 3
0x07e3: 8c 00 00 08 23 8c_control 2083
```

### 0x07f7..0x07fc

- Length: `5`
- Unknown bytes: `0`

```text
0x07f7: 8c 00 01 08 2e 8c_control 67630
```

### 0x0802..0x0807

- Length: `5`
- Unknown bytes: `0`

```text
0x0802: 8c 00 02 08 39 8c_control 133177
```

### 0x080d..0x0810

- Length: `3`
- Unknown bytes: `0`

```text
0x080d: f2             end_subscript
0x080e: f0             f0_control
0x080f: f2             end_subscript
```

## Interpretation

- This candidate length table covers most residual control bytes but still leaves unknown singletons.
- Clean 4-byte `ad/ac` and 5-byte `8c` records often point at nearby bytecode offsets, so they are strong branch/call candidates.
- `fe` consistently decodes as a 3-byte form in this slice.
- Remaining unknown bytes should be checked against neighboring spans before being added to the global opcode table.
