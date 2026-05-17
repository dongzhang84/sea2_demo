# João Opening Non-Motif Gaps

This reports bytecode gaps between `c0/cc/c8/c7` motif runs in `Snr1.chunk0.sub0`.
These gaps are candidates for branch, condition, state mutation, and non-motif text handling.

- Scenes: `40`
- Gaps: `41`
- Gap bytes: `804`
- Missing text ids inside motif range: `47`

## Missing Text IDs

- `87`: 哎呀，是$n先生呀，$s公爵正在找您呢．
- `88`: $n先生，公爵閣下有令要把您當作平民對待，所以請您不要再來皇宮了．
- `89`: $n先生，回公爵府了嗎？
- `90`: 〔菲利普主教〕\n哎唷，$n先生，$s公爵家有人要去航海嗎？
- `92`: 其實，我是來找有經驗的水手的．嘿，真難找．
- `93`: 啊，想起來了，從公爵府來的洛克先生正找您呢！
- `95`: 噢，$n先生，恩里克神父的事就拜託您啦．
- `96`: 另外，請把這些金幣作為資金的一部分使用吧．
- `97`: 接　　受\n捐　　款\n拒　　絕
- `101`: 噢，您是虔誠的人．上帝會保佑您的！
- `103`: 噢，您真謙虛啊！
- `104`: 〔菲利普主教〕\n噢，$n先生，感謝您光臨．
- `106`: 是啊，我要拜託您辦點事．
- `108`: 是啊，我聽說$n先生要出海，是嗎？
- `109`: 尋找傳說中的普萊斯特·約翰王國是我們基督教徒的使命，祝您成功．
- `110`: 還有一件事，我有個宿願，希望您能幫我實現．
- `111`: 恩里克，恩里克神父，這邊來．
- `113`: 這是從弗朗西斯科會派遣來的傳教士，叫恩里克．
- `114`: $n先生，您可能知道法王廳想向東方傳教吧．
- `115`: 拜託您把他送到日本吧．
- `125`: 少爺，我是受$s公爵之命造船的，到底是哪位要用這條船呀？
- `127`: 對了，想起來了．洛克正找您呢，說要您回公爵府．
- `129`: 原來是你呀，洛克，已經造好了．
- `130`: 按照萊昂公爵的命令，要把它造成同公爵首次坐的船一樣的拉丁級船．
- `131`: 船名是『海盧梅思2世』，是一種三角帆船，它易於操縱，適於初學者．
- `132`: 海盧梅思2世
- `133`: $n先生，你如果有什麼困難就去酒館吧．
- `134`: 那家的老闆娘叫卡蕾珞娃，聽說令尊年輕時曾得到過她的幫助．
- `136`: $n先生，菲利普主教正找您呢．
- `167`: 經常受到$s公爵的關照．
- `168`: 洛克先生從公爵府來找您了．
- `169`: 說起做生意，從本港買的岩鹽能在地中海賣高價．
- `170`: 和塞維爾的陶瓷器，可以在兩地之間做生意．
- `171`: $n先生，對不起，好像您沒有船．
- `172`: 請您有了船，再來吧！
- `173`: $n先生，洛克先生從公爵府來找您了．
- `174`: $n先生，有要代管的東西吧？
- `176`: 公爵府管家的麥克先生，叫我等您來了，把花劍給您．
- `177`: 費用已付，請拿走吧．
- `178`: 對了，請注意，武器沒有裝佩是不能使用的．
- `179`: 經常受到$s公爵的關照．
- `180`: 洛克先生從公爵府來找您了．
- `181`: $n先生，如有為難事，就去酒館．
- `182`: 因為聽說，公爵年輕時也得到過那家酒館女老闆的照顧．
- `183`: $n公子，真少見，穿著便服來的．
- `184`: 您是$s家的人，快出海了吧？
- `185`: $n先生，有公告說要把您當作平民對待，是真的嗎？

## Gaps

### gap_before_scene_00

- Offset: `0x0000..0x0008`
- Length: `8`
- Unknown bytes: `8`
- Embedded text refs: `0`

```text
0x0000: ad         db 173
0x0001: 00         db 0
0x0002: 01         db 1
0x0003: 2a         db 42
0x0004: ac         db 172
0x0005: 05         db 5
0x0006: 00         db 0
0x0007: 40         db 64
```

### gap_before_scene_01

- Offset: `0x0011..0x0024`
- Length: `19`
- Unknown bytes: `19`
- Embedded text refs: `0`

```text
0x0011: fe         db 254
0x0012: 02         db 2
0x0013: 62         db 98
0x0014: ad         db 173
0x0015: 05         db 5
0x0016: 01         db 1
0x0017: 2a         db 42
0x0018: ac         db 172
0x0019: 01         db 1
0x001a: 01         db 1
0x001b: 08         db 8
0x001c: 0f         db 15
0x001d: 01         db 1
0x001e: 07         db 7
0x001f: 8e         db 142
0x0020: 01         db 1
0x0021: 42         db 66
0x0022: 00         db 0
0x0023: f7         db 247
```

### gap_before_scene_02

- Offset: `0x00bd..0x00d0`
- Length: `19`
- Unknown bytes: `19`
- Embedded text refs: `0`

```text
0x00bd: dc         db 220
0x00be: 00         db 0
0x00bf: 06         db 6
0x00c0: 00         db 0
0x00c1: 3f         db 63
0x00c2: 1d         db 29
0x00c3: 00         db 0
0x00c4: 34         db 52
0x00c5: 2c         db 44
0x00c6: 01         db 1
0x00c7: 01         db 1
0x00c8: fe         db 254
0x00c9: 02         db 2
0x00ca: 62         db 98
0x00cb: 8f         db 143
0x00cc: 01         db 1
0x00cd: 41         db 65
0x00ce: 01         db 1
0x00cf: 08         db 8
```

### gap_before_scene_03

- Offset: `0x00d9..0x00e0`
- Length: `7`
- Unknown bytes: `7`
- Embedded text refs: `0`

```text
0x00d9: fe         db 254
0x00da: 02         db 2
0x00db: 62         db 98
0x00dc: ad         db 173
0x00dd: 01         db 1
0x00de: 01         db 1
0x00df: 2a         db 42
```

### gap_before_scene_04

- Offset: `0x00fb..0x0102`
- Length: `7`
- Unknown bytes: `7`
- Embedded text refs: `0`

```text
0x00fb: fe         db 254
0x00fc: 02         db 2
0x00fd: 62         db 98
0x00fe: ac         db 172
0x00ff: 00         db 0
0x0100: 02         db 2
0x0101: 62         db 98
```

### gap_before_scene_05

- Offset: `0x01fe..0x0201`
- Length: `3`
- Unknown bytes: `3`
- Embedded text refs: `0`

```text
0x01fe: f9         db 249
0x01ff: 05         db 5
0x0200: 05         db 5
```

### gap_before_scene_06

- Offset: `0x022e..0x0240`
- Length: `18`
- Unknown bytes: `17`
- Embedded text refs: `0`

```text
0x022e: fb         db 251
0x022f: 45         db 69
0x0230: 2c         db 44
0x0231: 00         db 0
0x0232: 01         db 1
0x0233: fe         db 254
0x0234: 02         db 2
0x0235: 62         db 98
0x0236: f8         db 248
0x0237: f2         end_subscript
0x0238: ac         db 172
0x0239: 00         db 0
0x023a: 02         db 2
0x023b: bf         db 191
0x023c: ad         db 173
0x023d: 04         db 4
0x023e: 02         db 2
0x023f: 75         db 117
```

### gap_before_scene_07

- Offset: `0x0249..0x024d`
- Length: `4`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x0249: ac         db 172
0x024a: 04         db 4
0x024b: 02         db 2
0x024c: be         db 190
```

### gap_before_scene_08

- Offset: `0x0271..0x0274`
- Length: `3`
- Unknown bytes: `3`
- Embedded text refs: `0`

```text
0x0271: c4         db 196
0x0272: ca         db 202
0x0273: 04         db 4
```

### gap_before_scene_09

- Offset: `0x028f..0x02a3`
- Length: `20`
- Unknown bytes: `18`
- Embedded text refs: `1`

```text
0x028f: 2c         db 44
0x0290: 04         db 4
0x0291: 01         db 1
0x0292: f8         db 248
0x0293: ad         db 173
0x0294: 00         db 0
0x0295: 03         db 3
0x0296: cb         db 203
0x0297: ad         db 173
0x0298: 05         db 5
0x0299: 02         db 2
0x029a: d9         db 217
0x029b: ac         db 172
0x029c: 01         db 1
0x029d: 02         db 2
0x029e: d9         db 217
0x029f: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x02a1: 00         db 0
0x02a2: 01         db 1
```

### gap_before_scene_10

- Offset: `0x02ac..0x02b5`
- Length: `9`
- Unknown bytes: `7`
- Embedded text refs: `1`

```text
0x02ac: f8         db 248
0x02ad: ac         db 172
0x02ae: 05         db 5
0x02af: 03         db 3
0x02b0: cb         db 203
0x02b1: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x02b3: 00         db 0
0x02b4: 01         db 1
```

### gap_before_scene_11

- Offset: `0x0333..0x0339`
- Length: `6`
- Unknown bytes: `4`
- Embedded text refs: `1`

```text
0x0333: 0c 00      show_text 0 ; 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
0x0335: 03         db 3
0x0336: e8         db 232
0x0337: e6         db 230
0x0338: 00         db 0
```

### gap_before_scene_12

- Offset: `0x0366..0x0367`
- Length: `1`
- Unknown bytes: `1`
- Embedded text refs: `0`

```text
0x0366: c4         db 196
```

### gap_before_scene_13

- Offset: `0x038b..0x03d2`
- Length: `71`
- Unknown bytes: `43`
- Embedded text refs: `1`

```text
0x038b: dc         db 220
0x038c: 00         db 0
0x038d: 05         db 5
0x038e: 00         db 0
0x038f: 0f         db 15
0x0390: 1d         db 29
0x0391: 00         db 0
0x0392: 64         db 100
0x0393: dc         db 220
0x0394: 00         db 0
0x0395: 05         db 5
0x0396: 01         db 1
0x0397: 0f         db 15
0x0398: 1d         db 29
0x0399: 00         db 0
0x039a: 64         db 100
0x039b: 2c         db 44
0x039c: 05         db 5
0x039d: 01         db 1
0x039e: f8         db 248
0x039f: f2         end_subscript
0x03a0: ac         db 172
0x03a1: 00         db 0
0x03a2: 03         db 3
0x03a3: d6         db 214
0x03a4: c0 00      c0 0
0x03a6: c8 00 57   c8 87
0x03a9: c7         c7
0x03aa: ad         db 173
0x03ab: 00         db 0
0x03ac: 03         db 3
0x03ad: e0         db 224
0x03ae: c0 00      c0 0
0x03b0: c8 00 58   c8 88
0x03b3: c7         c7
0x03b4: f8         db 248
0x03b5: f2         end_subscript
0x03b6: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x03b8: 00         db 0
0x03b9: 01         db 1
0x03ba: ac         db 172
0x03bb: 00         db 0
0x03bc: 04         db 4
0x03bd: 20         db 32
0x03be: ad         db 173
0x03bf: 07         db 7
0x03c0: 03         db 3
0x03c1: f4         db 244
0x03c2: c0 00      c0 0
0x03c4: c8 00 59   c8 89
0x03c7: c7         c7
0x03c8: ac         db 172
0x03c9: 07         db 7
0x03ca: 04         db 4
0x03cb: 1f         db 31
0x03cc: c0 00      c0 0
0x03ce: c8 00 5a   c8 90
0x03d1: c7         c7
```

### gap_before_scene_14

- Offset: `0x03db..0x03e7`
- Length: `12`
- Unknown bytes: `0`
- Embedded text refs: `0`

```text
0x03db: c0 00      c0 0
0x03dd: c8 00 5c   c8 92
0x03e0: c7         c7
0x03e1: c0 00      c0 0
0x03e3: c8 00 5d   c8 93
0x03e6: c7         c7
```

### gap_before_scene_15

- Offset: `0x03f0..0x0418`
- Length: `40`
- Unknown bytes: `28`
- Embedded text refs: `0`

```text
0x03f0: 2c         db 44
0x03f1: 07         db 7
0x03f2: 01         db 1
0x03f3: f8         db 248
0x03f4: ad         db 173
0x03f5: 00         db 0
0x03f6: 05         db 5
0x03f7: 5e         db 94
0x03f8: ad         db 173
0x03f9: 02         db 2
0x03fa: 04         db 4
0x03fb: 8f         db 143
0x03fc: c0 00      c0 0
0x03fe: c8 00 5f   c8 95
0x0401: c7         c7
0x0402: ac         db 172
0x0403: 08         db 8
0x0404: 04         db 4
0x0405: 8f         db 143
0x0406: 2c         db 44
0x0407: 08         db 8
0x0408: 01         db 1
0x0409: c0 00      c0 0
0x040b: c8 00 60   c8 96
0x040e: c7         c7
0x040f: c9         db 201
0x0410: 01         db 1
0x0411: 00         db 0
0x0412: 61         db 97
0x0413: 8c         db 140
0x0414: 01         db 1
0x0415: 00         db 0
0x0416: 04         db 4
0x0417: 53         db 83
```

### gap_before_scene_16

- Offset: `0x0421..0x042c`
- Length: `11`
- Unknown bytes: `9`
- Embedded text refs: `1`

```text
0x0421: 0c 00      show_text 0 ; 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
0x0423: 03         db 3
0x0424: e8         db 232
0x0425: e6         db 230
0x0426: 00         db 0
0x0427: 8c         db 140
0x0428: 01         db 1
0x0429: 01         db 1
0x042a: 04         db 4
0x042b: 7b         db 123
```

### gap_before_scene_17

- Offset: `0x043e..0x0454`
- Length: `22`
- Unknown bytes: `16`
- Embedded text refs: `0`

```text
0x043e: c0 00      c0 0
0x0440: c8 00 65   c8 101
0x0443: c7         c7
0x0444: dc         db 220
0x0445: 00         db 0
0x0446: 03         db 3
0x0447: 00         db 0
0x0448: 1c         db 28
0x0449: 4c         db 76
0x044a: 00         db 0
0x044b: 07         db 7
0x044c: 1d         db 29
0x044d: 00         db 0
0x044e: 64         db 100
0x044f: 8c         db 140
0x0450: 01         db 1
0x0451: 02         db 2
0x0452: 04         db 4
0x0453: 8f         db 143
```

### gap_before_scene_18

- Offset: `0x045d..0x0471`
- Length: `20`
- Unknown bytes: `8`
- Embedded text refs: `0`

```text
0x045d: c0 00      c0 0
0x045f: c8 00 67   c8 103
0x0462: c7         c7
0x0463: ac         db 172
0x0464: 02         db 2
0x0465: 05         db 5
0x0466: 5e         db 94
0x0467: c0 00      c0 0
0x0469: c8 00 68   c8 104
0x046c: c7         c7
0x046d: ac         db 172
0x046e: 07         db 7
0x046f: 04         db 4
0x0470: ac         db 172
```

### gap_before_scene_19

- Offset: `0x047a..0x0484`
- Length: `10`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x047a: c0 00      c0 0
0x047c: c8 00 6a   c8 106
0x047f: c7         c7
0x0480: ad         db 173
0x0481: 07         db 7
0x0482: 04         db 4
0x0483: cb         db 203
```

### gap_before_scene_20

- Offset: `0x048d..0x04a5`
- Length: `24`
- Unknown bytes: `0`
- Embedded text refs: `0`

```text
0x048d: c0 00      c0 0
0x048f: c8 00 6c   c8 108
0x0492: c7         c7
0x0493: c0 00      c0 0
0x0495: c8 00 6d   c8 109
0x0498: c7         c7
0x0499: c0 00      c0 0
0x049b: c8 00 6e   c8 110
0x049e: c7         c7
0x049f: c0 00      c0 0
0x04a1: c8 00 6f   c8 111
0x04a4: c7         c7
```

### gap_before_scene_21

- Offset: `0x04ae..0x04c0`
- Length: `18`
- Unknown bytes: `0`
- Embedded text refs: `0`

```text
0x04ae: c0 00      c0 0
0x04b0: c8 00 71   c8 113
0x04b3: c7         c7
0x04b4: c0 00      c0 0
0x04b6: c8 00 72   c8 114
0x04b9: c7         c7
0x04ba: c0 00      c0 0
0x04bc: c8 00 73   c8 115
0x04bf: c7         c7
```

### gap_before_scene_22

- Offset: `0x04f6..0x04f8`
- Length: `2`
- Unknown bytes: `2`
- Embedded text refs: `0`

```text
0x04f6: fb         db 251
0x04f7: 46         db 70
```

### gap_before_scene_23

- Offset: `0x0513..0x0541`
- Length: `46`
- Unknown bytes: `35`
- Embedded text refs: `2`

```text
0x0513: dc         db 220
0x0514: 00         db 0
0x0515: 0c 62      show_text 98 ; 謝謝，那我就不客氣了．
0x0517: 15         db 21
0x0518: 05         db 5
0x0519: 01         db 1
0x051a: 00         db 0
0x051b: 6c         db 108
0x051c: 01         db 1
0x051d: 20         db 32
0x051e: 11         db 17
0x051f: 00         db 0
0x0520: 01         db 1
0x0521: dc         db 220
0x0522: 00         db 0
0x0523: 0c 63      show_text 99 ; 不，我不能要主教大人的錢．
0x0525: 15         db 21
0x0526: 05         db 5
0x0527: 01         db 1
0x0528: 00         db 0
0x0529: 6c         db 108
0x052a: 01         db 1
0x052b: 20         db 32
0x052c: 11         db 17
0x052d: 00         db 0
0x052e: 01         db 1
0x052f: 2c         db 44
0x0530: 02         db 2
0x0531: 01         db 1
0x0532: f2         end_subscript
0x0533: ac         db 172
0x0534: 03         db 3
0x0535: 05         db 5
0x0536: a3         db 163
0x0537: ac         db 172
0x0538: 00         db 0
0x0539: 05         db 5
0x053a: 7c         db 124
0x053b: c0 00      c0 0
0x053d: c8 00 7d   c8 125
0x0540: c7         c7
```

### gap_before_scene_24

- Offset: `0x054a..0x0554`
- Length: `10`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x054a: c0 00      c0 0
0x054c: c8 00 7f   c8 127
0x054f: c7         c7
0x0550: ad         db 173
0x0551: 00         db 0
0x0552: 05         db 5
0x0553: a2         db 162
```

### gap_before_scene_25

- Offset: `0x055d..0x0594`
- Length: `55`
- Unknown bytes: `22`
- Embedded text refs: `1`

```text
0x055d: c0 00      c0 0
0x055f: c8 00 81   c8 129
0x0562: c7         c7
0x0563: c0 00      c0 0
0x0565: c8 00 82   c8 130
0x0568: c7         c7
0x0569: c0 00      c0 0
0x056b: c8 00 83   c8 131
0x056e: c7         c7
0x056f: fa         db 250
0x0570: 05         db 5
0x0571: 00         db 0
0x0572: 84         db 132
0x0573: 2c         db 44
0x0574: 03         db 3
0x0575: 01         db 1
0x0576: f8         db 248
0x0577: f2         end_subscript
0x0578: ac         db 172
0x0579: 00         db 0
0x057a: 05         db 5
0x057b: b8         db 184
0x057c: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x057e: 00         db 0
0x057f: 01         db 1
0x0580: c0 00      c0 0
0x0582: c8 00 85   c8 133
0x0585: c7         c7
0x0586: c0 00      c0 0
0x0588: c8 00 86   c8 134
0x058b: c7         c7
0x058c: ad         db 173
0x058d: 00         db 0
0x058e: 07         db 7
0x058f: 48         db 72
0x0590: ac         db 172
0x0591: 03         db 3
0x0592: 05         db 5
0x0593: cc         db 204
```

### gap_before_scene_26

- Offset: `0x059d..0x05ae`
- Length: `17`
- Unknown bytes: `11`
- Embedded text refs: `0`

```text
0x059d: fe         db 254
0x059e: 07         db 7
0x059f: 48         db 72
0x05a0: ac         db 172
0x05a1: 02         db 2
0x05a2: 05         db 5
0x05a3: f4         db 244
0x05a4: c0 00      c0 0
0x05a6: c8 00 88   c8 136
0x05a9: c7         c7
0x05aa: ac         db 172
0x05ab: 07         db 7
0x05ac: 05         db 5
0x05ad: e3         db 227
```

### gap_before_scene_27

- Offset: `0x05b7..0x05bb`
- Length: `4`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x05b7: ad         db 173
0x05b8: 07         db 7
0x05b9: 05         db 5
0x05ba: f0         db 240
```

### gap_before_scene_28

- Offset: `0x05c4..0x05d4`
- Length: `16`
- Unknown bytes: `16`
- Embedded text refs: `0`

```text
0x05c4: f8         db 248
0x05c5: fe         db 254
0x05c6: 07         db 7
0x05c7: 48         db 72
0x05c8: ac         db 172
0x05c9: 01         db 1
0x05ca: 06         db 6
0x05cb: 26         db 38
0x05cc: ac         db 172
0x05cd: 05         db 5
0x05ce: 06         db 6
0x05cf: 16         db 22
0x05d0: ac         db 172
0x05d1: 08         db 8
0x05d2: 06         db 6
0x05d3: 09         db 9
```

### gap_before_scene_29

- Offset: `0x05dd..0x05e1`
- Length: `4`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x05dd: ad         db 173
0x05de: 08         db 8
0x05df: 06         db 6
0x05e0: 16         db 22
```

### gap_before_scene_30

- Offset: `0x05ea..0x05ee`
- Length: `4`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x05ea: ad         db 173
0x05eb: 05         db 5
0x05ec: 06         db 6
0x05ed: 23         db 35
```

### gap_before_scene_31

- Offset: `0x05f7..0x05fe`
- Length: `7`
- Unknown bytes: `7`
- Embedded text refs: `0`

```text
0x05f7: fe         db 254
0x05f8: 07         db 7
0x05f9: 48         db 72
0x05fa: ac         db 172
0x05fb: 0a         db 10
0x05fc: 07         db 7
0x05fd: 48         db 72
```

### gap_before_scene_32

- Offset: `0x068e..0x069b`
- Length: `13`
- Unknown bytes: `9`
- Embedded text refs: `2`

```text
0x068e: dc         db 220
0x068f: 0b         db 11
0x0690: 03         db 3
0x0691: 46         db 70
0x0692: 2e         db 46
0x0693: 05         db 5
0x0694: 0c 0b      show_text 11 ; 因為沒有比航海更能鍛練男子漢的．
0x0696: 8d         db 141
0x0697: 0c 04      show_text 4 ; 可是，船長，我聽說公爵是跟某個貴族之間有恩怨呀．
0x0699: 07         db 7
0x069a: 3c         db 60
```

### gap_before_scene_33

- Offset: `0x06a4..0x06aa`
- Length: `6`
- Unknown bytes: `6`
- Embedded text refs: `0`

```text
0x06a4: e9         db 233
0x06a5: 0b         db 11
0x06a6: ad         db 173
0x06a7: 0b         db 11
0x06a8: 07         db 7
0x06a9: 17         db 23
```

### gap_before_scene_34

- Offset: `0x06b3..0x06c8`
- Length: `21`
- Unknown bytes: `17`
- Embedded text refs: `2`

```text
0x06b3: dc         db 220
0x06b4: 00         db 0
0x06b5: 03         db 3
0x06b6: 46         db 70
0x06b7: 2e         db 46
0x06b8: 1d         db 29
0x06b9: 00         db 0
0x06ba: 04         db 4
0x06bb: dc         db 220
0x06bc: 0b         db 11
0x06bd: 03         db 3
0x06be: 45         db 69
0x06bf: 2e         db 46
0x06c0: 05         db 5
0x06c1: 0c 0b      show_text 11 ; 因為沒有比航海更能鍛練男子漢的．
0x06c3: 8d         db 141
0x06c4: 0c 03      show_text 3 ; 太太，這是$s家人的呀！
0x06c6: 07         db 7
0x06c7: 05         db 5
```

### gap_before_scene_35

- Offset: `0x06d1..0x06d9`
- Length: `8`
- Unknown bytes: `8`
- Embedded text refs: `0`

```text
0x06d1: dc         db 220
0x06d2: 00         db 0
0x06d3: 03         db 3
0x06d4: 45         db 69
0x06d5: 2e         db 46
0x06d6: 1d         db 29
0x06d7: 00         db 0
0x06d8: 03         db 3
```

### gap_before_scene_36

- Offset: `0x06eb..0x06ef`
- Length: `4`
- Unknown bytes: `4`
- Embedded text refs: `0`

```text
0x06eb: ac         db 172
0x06ec: 0b         db 11
0x06ed: 07         db 7
0x06ee: 36         db 54
```

### gap_before_scene_37

- Offset: `0x070a..0x0710`
- Length: `6`
- Unknown bytes: `6`
- Embedded text refs: `0`

```text
0x070a: 2c         db 44
0x070b: 0a         db 10
0x070c: 01         db 1
0x070d: fe         db 254
0x070e: 07         db 7
0x070f: 48         db 72
```

### gap_before_scene_38

- Offset: `0x0719..0x076d`
- Length: `84`
- Unknown bytes: `32`
- Embedded text refs: `1`

```text
0x0719: 2c         db 44
0x071a: 0a         db 10
0x071b: 01         db 1
0x071c: f2         end_subscript
0x071d: ac         db 172
0x071e: 00         db 0
0x071f: 07         db 7
0x0720: 66         db 102
0x0721: c0 00      c0 0
0x0723: c8 00 a7   c8 167
0x0726: c7         c7
0x0727: c0 00      c0 0
0x0729: c8 00 a8   c8 168
0x072c: c7         c7
0x072d: c0 00      c0 0
0x072f: c8 00 a9   c8 169
0x0732: c7         c7
0x0733: c0 00      c0 0
0x0735: c8 00 aa   c8 170
0x0738: c7         c7
0x0739: f8         db 248
0x073a: ad         db 173
0x073b: 00         db 0
0x073c: 07         db 7
0x073d: 7b         db 123
0x073e: ac         db 172
0x073f: 03         db 3
0x0740: 07         db 7
0x0741: 7b         db 123
0x0742: c0 00      c0 0
0x0744: c8 00 ab   c8 171
0x0747: c7         c7
0x0748: c0 00      c0 0
0x074a: c8 00 ac   c8 172
0x074d: c7         c7
0x074e: f8         db 248
0x074f: f2         end_subscript
0x0750: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x0752: 00         db 0
0x0753: 01         db 1
0x0754: ac         db 172
0x0755: 00         db 0
0x0756: 07         db 7
0x0757: 8b         db 139
0x0758: c0 00      c0 0
0x075a: c8 00 ad   c8 173
0x075d: c7         c7
0x075e: f8         db 248
0x075f: ad         db 173
0x0760: 00         db 0
0x0761: 07         db 7
0x0762: c6         db 198
0x0763: ac         db 172
0x0764: 09         db 9
0x0765: 07         db 7
0x0766: bc         db 188
0x0767: c0 00      c0 0
0x0769: c8 00 ae   c8 174
0x076c: c7         c7
```

### gap_before_scene_39

- Offset: `0x0776..0x07ee`
- Length: `120`
- Unknown bytes: `57`
- Embedded text refs: `1`

```text
0x0776: c0 00      c0 0
0x0778: c8 00 b0   c8 176
0x077b: c7         c7
0x077c: c0 00      c0 0
0x077e: c8 00 b1   c8 177
0x0781: c7         c7
0x0782: dc         db 220
0x0783: 00         db 0
0x0784: 06         db 6
0x0785: 00         db 0
0x0786: 3f         db 63
0x0787: 4c         db 76
0x0788: 00         db 0
0x0789: 01         db 1
0x078a: 1d         db 29
0x078b: 00         db 0
0x078c: 03         db 3
0x078d: 2c         db 44
0x078e: 09         db 9
0x078f: 01         db 1
0x0790: ad         db 173
0x0791: 09         db 9
0x0792: 07         db 7
0x0793: c6         db 198
0x0794: c0 00      c0 0
0x0796: c8 00 b2   c8 178
0x0799: c7         c7
0x079a: f2         end_subscript
0x079b: 0c 3f      show_text 63 ; 太太要您晚上10點到12點之間去公爵府．
0x079d: 00         db 0
0x079e: 01         db 1
0x079f: ac         db 172
0x07a0: 00         db 0
0x07a1: 08         db 8
0x07a2: 07         db 7
0x07a3: eb         db 235
0x07a4: 00         db 0
0x07a5: 00         db 0
0x07a6: 03         db 3
0x07a7: 8c         db 140
0x07a8: 00         db 0
0x07a9: 00         db 0
0x07aa: 07         db 7
0x07ab: e4         db 228
0x07ac: c0 00      c0 0
0x07ae: c8 00 b3   c8 179
0x07b1: c7         c7
0x07b2: c0 00      c0 0
0x07b4: c8 00 b4   c8 180
0x07b7: c7         c7
0x07b8: 8c         db 140
0x07b9: 00         db 0
0x07ba: 01         db 1
0x07bb: 07         db 7
0x07bc: f5         db 245
0x07bd: c0 00      c0 0
0x07bf: c8 00 b5   c8 181
0x07c2: c7         c7
0x07c3: c0 00      c0 0
0x07c5: c8 00 b6   c8 182
0x07c8: c7         c7
0x07c9: 8c         db 140
0x07ca: 00         db 0
0x07cb: 02         db 2
0x07cc: 08         db 8
0x07cd: 06         db 6
0x07ce: c0 00      c0 0
0x07d0: c8 00 b7   c8 183
0x07d3: c7         c7
0x07d4: c0 00      c0 0
0x07d6: c8 00 b8   c8 184
0x07d9: c7         c7
0x07da: f8         db 248
0x07db: ad         db 173
0x07dc: 00         db 0
0x07dd: 08         db 8
0x07de: 39         db 57
0x07df: eb         db 235
0x07e0: 00         db 0
0x07e1: 00         db 0
0x07e2: 03         db 3
0x07e3: 8c         db 140
0x07e4: 00         db 0
0x07e5: 00         db 0
0x07e6: 08         db 8
0x07e7: 23         db 35
0x07e8: c0 00      c0 0
0x07ea: c8 00 b9   c8 185
0x07ed: c7         c7
```

### gap_after_last_scene

- Offset: `0x07f7..0x0810`
- Length: `25`
- Unknown bytes: `11`
- Embedded text refs: `0`

```text
0x07f7: 8c         db 140
0x07f8: 00         db 0
0x07f9: 01         db 1
0x07fa: 08         db 8
0x07fb: 2e         db 46
0x07fc: c0 00      c0 0
0x07fe: c8 00 bb   c8 187
0x0801: c7         c7
0x0802: 8c         db 140
0x0803: 00         db 0
0x0804: 02         db 2
0x0805: 08         db 8
0x0806: 39         db 57
0x0807: c0 00      c0 0
0x0809: c8 00 bc   c8 188
0x080c: c7         c7
0x080d: f2         end_subscript
0x080e: f0         db 240
0x080f: f2         end_subscript
```

