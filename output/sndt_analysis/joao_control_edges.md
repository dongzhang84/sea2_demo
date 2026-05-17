# Joao Opening Control Edge Candidates

This report tests whether control operands in the Joao opening subscript point at known timeline byte ranges.

## Summary

- code_len_hex: 0x0810
- timeline_items: 87
- control_instructions: 68
- candidate_edges: 526
- match_counts: `{'inside_item': 128, 'no_match': 310, 'near_item': 59, 'exact_end': 4, 'exact_start': 25}`
- preferred_match_counts: `{'inside_item': 50, 'exact_end': 3, 'exact_start': 10, 'near_item': 4, 'no_match': 1}`

## Candidate Interpretation Scores

| op:candidate | total | in range | exact start | exact end | inside | near | none |
|---|---:|---:|---:|---:|---:|---:|---:|
| 8c_control:high16_be | 9 | 9 | 1 | 0 | 0 | 2 | 6 |
| 8c_control:high16_le | 9 | 9 | 1 | 0 | 0 | 5 | 3 |
| 8c_control:low16_be | 9 | 6 | 0 | 0 | 3 | 3 | 3 |
| 8c_control:low16_le | 9 | 1 | 0 | 0 | 1 | 0 | 8 |
| 8c_control:low24_be | 9 | 2 | 0 | 0 | 0 | 2 | 7 |
| 8c_control:low24_le | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| 8c_control:operand_be | 9 | 1 | 0 | 0 | 0 | 1 | 8 |
| 8c_control:operand_le | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| ac_control:high16_be | 29 | 26 | 2 | 1 | 12 | 8 | 6 |
| ac_control:high16_le | 29 | 29 | 1 | 1 | 19 | 8 | 0 |
| ac_control:low16_be | 29 | 29 | 2 | 0 | 19 | 6 | 2 |
| ac_control:low16_le | 29 | 2 | 0 | 0 | 2 | 0 | 27 |
| ac_control:low24_be | 29 | 9 | 1 | 0 | 4 | 3 | 21 |
| ac_control:low24_le | 29 | 0 | 0 | 0 | 0 | 0 | 29 |
| ac_control:operand_be | 29 | 9 | 1 | 0 | 4 | 3 | 21 |
| ac_control:operand_le | 29 | 0 | 0 | 0 | 0 | 0 | 29 |
| ad_control:high16_be | 21 | 19 | 1 | 1 | 7 | 7 | 5 |
| ad_control:high16_le | 21 | 21 | 0 | 1 | 16 | 4 | 0 |
| ad_control:low16_be | 21 | 20 | 1 | 0 | 16 | 3 | 1 |
| ad_control:low16_le | 21 | 0 | 0 | 0 | 0 | 0 | 21 |
| ad_control:low24_be | 21 | 8 | 1 | 0 | 5 | 2 | 13 |
| ad_control:low24_le | 21 | 0 | 0 | 0 | 0 | 0 | 21 |
| ad_control:operand_be | 21 | 8 | 1 | 0 | 5 | 2 | 13 |
| ad_control:operand_le | 21 | 0 | 0 | 0 | 0 | 0 | 21 |
| fe_control:high16_be | 9 | 9 | 4 | 0 | 5 | 0 | 0 |
| fe_control:high16_le | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| fe_control:low16_be | 9 | 9 | 4 | 0 | 5 | 0 | 0 |
| fe_control:low16_le | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| fe_control:operand_be | 9 | 9 | 4 | 0 | 5 | 0 | 0 |
| fe_control:operand_le | 9 | 0 | 0 | 0 | 0 | 0 | 9 |

## Preferred Edge Interpretations

Preferred interpretations bias toward big-endian operand/low16 forms that look like script pointers. Near matches are kept because some operands may point to the byte just before a text motif or to a small control prelude.

| source | bytes | preferred candidate | target | match | timeline item | nearest |
|---|---|---|---:|---|---|---|
| 0x0000 ad_control | ad 00 01 2a | operand_be | 0x012a | inside_item | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=40 |
| 0x0004 ac_control | ac 05 00 40 | low16_be | 0x0040 | inside_item | Snr1.chunk0.sub0.run1 / motif_scene / text=[1, 17] / $s公爵夫人 / 老水手洛克 | start 0x0024 d=28 |
| 0x0011 fe_control | fe 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x0014 ad_control | ad 05 01 2a | low16_be | 0x012a | inside_item | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=40 |
| 0x0018 ac_control | ac 01 01 08 | low16_be | 0x0108 | inside_item | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=6 |
| 0x00c8 fe_control | fe 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x00d9 fe_control | fe 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x00dc ad_control | ad 01 01 2a | low16_be | 0x012a | inside_item | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=40 |
| 0x00fb fe_control | fe 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x00fe ac_control | ac 00 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x0233 fe_control | fe 02 62 | operand_be | 0x0262 | inside_item | Snr1.chunk0.sub0.run7 / motif_scene / text=[56, 59] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 | end 0x0271 d=15 |
| 0x0238 ac_control | ac 00 02 bf | operand_be | 0x02bf | inside_item | Snr1.chunk0.sub0.run10 / motif_scene / text=[64, 77] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 / 老水手洛克 | start 0x02b5 d=10 |
| 0x023c ad_control | ad 04 02 75 | high16_be | 0x0402 | exact_end | Snr1.chunk0.sub0.short50 / short_text / text=95 | end 0x0402 d=0 |
| 0x0249 ac_control | ac 04 02 be | high16_be | 0x0402 | exact_end | Snr1.chunk0.sub0.short50 / short_text / text=95 | end 0x0402 d=0 |
| 0x0293 ad_control | ad 00 03 cb | high16_le | 0x0300 | inside_item | Snr1.chunk0.sub0.run10 / motif_scene / text=[64, 77] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 / 老水手洛克 | end 0x0333 d=51 |
| 0x0297 ad_control | ad 05 02 d9 | low16_be | 0x02d9 | inside_item | Snr1.chunk0.sub0.run10 / motif_scene / text=[64, 77] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 / 老水手洛克 | start 0x02b5 d=36 |
| 0x029b ac_control | ac 01 02 d9 | high16_be | 0x0102 | exact_start | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=0 |
| 0x02ad ac_control | ac 05 03 cb | high16_be | 0x0503 | inside_item | Snr1.chunk0.sub0.run22 / motif_scene / text=[122, 124] / 老水手洛克 | start 0x04f8 d=11 |
| 0x03a0 ac_control | ac 00 03 d6 | operand_be | 0x03d6 | inside_item | Snr1.chunk0.sub0.run13 / motif_scene / text=[91, 91] / João self/default lines | end 0x03d2 d=4 |
| 0x03aa ad_control | ad 00 03 e0 | operand_be | 0x03e0 | inside_item | Snr1.chunk0.sub0.short48 / short_text / text=92 | end 0x03e1 d=1 |
| 0x03ba ac_control | ac 00 04 20 | operand_be | 0x0420 | inside_item | Snr1.chunk0.sub0.run15 / motif_scene / text=[98, 98] / João self/default lines | end 0x0421 d=1 |
| 0x03be ad_control | ad 07 03 f4 | high16_be | 0x0703 | inside_item | Snr1.chunk0.sub0.run36 / motif_scene / text=[163, 165] / 恩里克神父 | end 0x070a d=7 |
| 0x03c8 ac_control | ac 07 04 1f | low16_be | 0x041f | inside_item | Snr1.chunk0.sub0.run15 / motif_scene / text=[98, 98] / João self/default lines | end 0x0421 d=2 |
| 0x03f4 ad_control | ad 00 05 5e | operand_be | 0x055e | inside_item | Snr1.chunk0.sub0.short65 / short_text / text=129 | end 0x055d d=1 |
| 0x03f8 ad_control | ad 02 04 8f | high16_le | 0x0402 | exact_end | Snr1.chunk0.sub0.short50 / short_text / text=95 | end 0x0402 d=0 |
| 0x0402 ac_control | ac 08 04 8f | low16_be | 0x048f | inside_item | Snr1.chunk0.sub0.short56 / short_text / text=108 | end 0x048d d=2 |
| 0x0413 8c_control | 8c 01 00 04 53 | low16_be | 0x0453 | near_item | Snr1.chunk0.sub0.run17 / motif_scene / text=[102, 102] / João self/default lines | start 0x0454 d=1 |
| 0x0427 8c_control | 8c 01 01 04 7b | low16_be | 0x047b | inside_item | Snr1.chunk0.sub0.short55 / short_text / text=106 | end 0x047a d=1 |
| 0x044f 8c_control | 8c 01 02 04 8f | high16_be | 0x0102 | exact_start | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=0 |
| 0x0463 ac_control | ac 02 05 5e | low16_be | 0x055e | inside_item | Snr1.chunk0.sub0.short65 / short_text / text=129 | end 0x055d d=1 |
| 0x046d ac_control | ac 07 04 ac | low16_be | 0x04ac | inside_item | Snr1.chunk0.sub0.run20 / motif_scene / text=[112, 112] / 恩里克神父 | end 0x04ae d=2 |
| 0x0480 ad_control | ad 07 04 cb | low16_be | 0x04cb | inside_item | Snr1.chunk0.sub0.run21 / motif_scene / text=[116, 121] / 恩里克神父 | end 0x04c0 d=11 |
| 0x0533 ac_control | ac 03 05 a3 | high16_be | 0x0305 | inside_item | Snr1.chunk0.sub0.run10 / motif_scene / text=[64, 77] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 / 老水手洛克 | end 0x0333 d=46 |
| 0x0537 ac_control | ac 00 05 7c | high16_le | 0x0500 | inside_item | Snr1.chunk0.sub0.run22 / motif_scene / text=[122, 124] / 老水手洛克 | start 0x04f8 d=8 |
| 0x0550 ad_control | ad 00 05 a2 | high16_le | 0x0500 | inside_item | Snr1.chunk0.sub0.run22 / motif_scene / text=[122, 124] / 老水手洛克 | start 0x04f8 d=8 |
| 0x0578 ac_control | ac 00 05 b8 | high16_le | 0x0500 | inside_item | Snr1.chunk0.sub0.run22 / motif_scene / text=[122, 124] / 老水手洛克 | start 0x04f8 d=8 |
| 0x058c ad_control | ad 00 07 48 | operand_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x0590 ac_control | ac 03 05 cc | high16_be | 0x0305 | inside_item | Snr1.chunk0.sub0.run10 / motif_scene / text=[64, 77] / 紅鯨亭女老闆卡蕾珞娃 / 歌女路琪亞 / 老水手洛克 | end 0x0333 d=46 |
| 0x059d fe_control | fe 07 48 | operand_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x05a0 ac_control | ac 02 05 f4 | low16_be | 0x05f4 | inside_item | Snr1.chunk0.sub0.run30 / motif_scene / text=[141, 141] / 老水手洛克 | end 0x05f7 d=3 |
| 0x05aa ac_control | ac 07 05 e3 | low16_be | 0x05e3 | inside_item | Snr1.chunk0.sub0.run29 / motif_scene / text=[140, 140] / 老水手洛克 | start 0x05e1 d=2 |
| 0x05b7 ad_control | ad 07 05 f0 | low16_be | 0x05f0 | inside_item | Snr1.chunk0.sub0.run30 / motif_scene / text=[141, 141] / 老水手洛克 | start 0x05ee d=2 |
| 0x05c5 fe_control | fe 07 48 | operand_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x05c8 ac_control | ac 01 06 26 | low16_be | 0x0626 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=40 |
| 0x05cc ac_control | ac 05 06 16 | low16_be | 0x0616 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=24 |
| 0x05d0 ac_control | ac 08 06 09 | low16_be | 0x0609 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=11 |
| 0x05dd ad_control | ad 08 06 16 | low16_be | 0x0616 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=24 |
| 0x05ea ad_control | ad 05 06 23 | low16_be | 0x0623 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=37 |
| 0x05f7 fe_control | fe 07 48 | operand_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x05fa ac_control | ac 0a 07 48 | low16_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x06a6 ad_control | ad 0b 07 17 | low16_be | 0x0717 | inside_item | Snr1.chunk0.sub0.run37 / motif_scene / text=[166, 166] / 老水手洛克 | end 0x0719 d=2 |
| 0x06eb ac_control | ac 0b 07 36 | low16_be | 0x0736 | inside_item | Snr1.chunk0.sub0.short74 / short_text / text=170 | end 0x0733 d=3 |
| 0x070d fe_control | fe 07 48 | operand_be | 0x0748 | exact_start | Snr1.chunk0.sub0.short76 / short_text / text=172 | end 0x0748 d=0 |
| 0x071d ac_control | ac 00 07 66 | high16_le | 0x0700 | inside_item | Snr1.chunk0.sub0.run36 / motif_scene / text=[163, 165] / 恩里克神父 | end 0x070a d=10 |
| 0x073a ad_control | ad 00 07 7b | operand_be | 0x077b | inside_item | Snr1.chunk0.sub0.short79 / short_text / text=176 | end 0x077c d=1 |
| 0x073e ac_control | ac 03 07 7b | low16_be | 0x077b | inside_item | Snr1.chunk0.sub0.short79 / short_text / text=176 | end 0x077c d=1 |
| 0x0754 ac_control | ac 00 07 8b | high16_le | 0x0700 | inside_item | Snr1.chunk0.sub0.run36 / motif_scene / text=[163, 165] / 恩里克神父 | end 0x070a d=10 |
| 0x075f ad_control | ad 00 07 c6 | operand_be | 0x07c6 | inside_item | Snr1.chunk0.sub0.short85 / short_text / text=182 | end 0x07c3 d=3 |
| 0x0763 ac_control | ac 09 07 bc | high16_le | 0x0709 | inside_item | Snr1.chunk0.sub0.run36 / motif_scene / text=[163, 165] / 恩里克神父 | end 0x070a d=1 |
| 0x0790 ad_control | ad 09 07 c6 | low16_be | 0x07c6 | inside_item | Snr1.chunk0.sub0.short85 / short_text / text=182 | end 0x07c3 d=3 |
| 0x079f ac_control | ac 00 08 07 | operand_be | 0x0807 | exact_start | Snr1.chunk0.sub0.short90 / short_text / text=188 | start 0x0807 d=0 |
| 0x07a7 8c_control | 8c 00 00 07 e4 | low16_be | 0x07e4 | near_item | Snr1.chunk0.sub0.short88 / short_text / text=185 | start 0x07e8 d=4 |
| 0x07b8 8c_control | 8c 00 01 07 f5 | low16_be | 0x07f5 | inside_item | Snr1.chunk0.sub0.run39 / motif_scene / text=[186, 186] / João self/default lines | end 0x07f7 d=2 |
| 0x07c9 8c_control | 8c 00 02 08 06 | low16_le | 0x0608 | inside_item | Snr1.chunk0.sub0.run31 / motif_scene / text=[142, 157] / 老水手洛克 / 恩里克神父 | start 0x05fe d=10 |
| 0x07db ad_control | ad 00 08 39 | high16_be | 0x0008 | exact_start | Snr1.chunk0.sub0.run0 / motif_scene / text=[0, 0] / 管家麥克 | start 0x0008 d=0 |
| 0x07e3 8c_control | 8c 00 00 08 23 | high16_be | 0x0000 | no_match | Snr1.chunk0.sub0.run0 / motif_scene / text=[0, 0] / 管家麥克 | start 0x0008 d=8 |
| 0x07f7 8c_control | 8c 00 01 08 2e | high16_le | 0x0100 | near_item | Snr1.chunk0.sub0.run4 / motif_scene / text=[22, 49] / $s公爵 | start 0x0102 d=2 |
| 0x0802 8c_control | 8c 00 02 08 39 | high16_le | 0x0200 | near_item | Snr1.chunk0.sub0.run5 / motif_scene / text=[50, 54] / $s公爵 / 老水手洛克 | start 0x0201 d=1 |

