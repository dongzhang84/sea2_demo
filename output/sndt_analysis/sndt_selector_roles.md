# SNDT Motif selector Role Analysis

`selector` is the operand after `c0` in `c0 selector cc cc_arg c8 text_id c7`.

## Counts

- selector `1`: `1728`
- selector `2`: `1721`

## Transitions Within Subscripts

- `1 -> 2`: 948
- `2 -> 1`: 874
- `2 -> 2`: 762
- `1 -> 1`: 724

## By SNDT File

| SNDT | selector 1 | selector 2 |
|---|---:|---:|
| Snr1 | 578 | 492 |
| Snr2 | 451 | 402 |
| Snr3 | 223 | 233 |
| Snr4 | 119 | 99 |
| Snr5 | 107 | 144 |
| Snr6 | 250 | 351 |

## Selector Profiles

### Selector 1

Top cc_arg values:

- `cc=34`: 161
- `cc=36`: 117
- `cc=31`: 102
- `cc=1`: 93
- `cc=99`: 89
- `cc=6`: 87
- `cc=40`: 72
- `cc=97`: 69
- `cc=15`: 65
- `cc=25`: 64
- `cc=0`: 63
- `cc=4`: 63

Top resolved speakers:

- `管家麥克`: 53
- `皮耶德·康迪`: 22
- `$s公爵`: 20
- `艾澤格司令`: 19
- `老水手洛克`: 17
- `地理學家梅爾卡特`: 17
- `約翰·法雷爾`: 17
- `海員馬休·路易`: 16
- `阿爾伯特皇太子`: 14
- `麥克白`: 12
- `亨利8世`: 12
- `朋友薩達姆`: 12

Examples:

- `Snr1.chunk0.sub0:0x0008` cc=6 speaker=管家麥克 text=0: 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
- `Snr1.chunk0.sub0:0x0024` cc=19 speaker=$s公爵夫人 text=1: 〔$s公爵夫人〕\n哎呀，$n，這事已聽你父親說了，突然要你走出家，真殘酷呀！
- `Snr1.chunk0.sub0:0x0048` cc=19 speaker=$s公爵夫人 text=5: 是啊，聽說跟馬丁內斯侯爵意見不和．
- `Snr1.chunk0.sub0:0x0063` cc=19 speaker=$s公爵夫人 text=8: 哎呀，洛克，你雖然長相平凡，但頭腦卻很不錯呀！
- `Snr1.chunk0.sub0:0x0087` cc=19 speaker=$s公爵夫人 text=12: 好吧，我就把$n託給你了．
- `Snr1.chunk0.sub0:0x0090` cc=19 speaker=$s公爵夫人 text=13: 另外，$n，聽路琪亞小姐說你現在還沒有多少航海的資金，是麼？
- `Snr1.chunk0.sub0:0x0099` cc=19 speaker=$s公爵夫人 text=14: 由於事情很突然，所以沒有準備好金幣，把這個給你吧．
- `Snr1.chunk0.sub0:0x00a2` cc=19 speaker=$s公爵夫人 text=15: 這是以前我跟你父親要的銀髮飾．
- `Snr1.chunk0.sub0:0x00ab` cc=19 speaker=$s公爵夫人 text=16: 把它賣掉當作資金吧，但對你爸要保密．
- `Snr1.chunk0.sub0:0x00b4` cc=19 speaker=$s公爵夫人 text=17: $n，一定要多加小心，上帝保佑你．
- `Snr1.chunk0.sub0:0x00d0` cc=6 speaker=管家麥克 text=18: 〔管家麥克〕\n$n，很對不起，公爵有令，不讓您進家門．
- `Snr1.chunk0.sub0:0x00e0` cc=6 speaker=管家麥克 text=19: 〔管家麥克〕\n$n，很對不起，公爵有令，不讓您進家門．
- `Snr1.chunk0.sub0:0x00f2` cc=6 speaker=管家麥克 text=21: 大海像瞬間即改變其表情的怪物一樣危險．$n先生，請您一定要多加小心啊．
- `Snr1.chunk0.sub0:0x010b` cc=18 speaker=$s公爵 text=23: 〔$s公爵〕\n噢，是$n啊，你現在劍術練得如何了？
- `Snr1.chunk0.sub0:0x011d` cc=18 speaker=$s公爵 text=25: 是嗎，那麼航海術呢，學好啦？
- `Snr1.chunk0.sub0:0x012f` cc=18 speaker=$s公爵 text=27: 是嗎，那麼對地理學呢，擅長嗎？

### Selector 2

Top cc_arg values:

- `cc=0`: 360
- `cc=1`: 283
- `cc=5`: 276
- `cc=2`: 179
- `cc=4`: 124
- `cc=31`: 95
- `cc=3`: 68
- `cc=34`: 66
- `cc=35`: 58
- `cc=127`: 35
- `cc=36`: 27
- `cc=40`: 22

Top resolved speakers:

- `老水手洛克`: 12
- `女海盜卡特琳娜`: 12
- `翻譯勞拉`: 12
- `蘇萊曼大帝`: 11
- `桑多中尉`: 10
- `搭船者`: 5
- `桑多`: 5
- `恩里克神父`: 4
- `紀德`: 4
- `馬丁內斯侯爵`: 3
- `阿爾伯特皇太子`: 3
- `塔法利一世`: 3

Examples:

- `Snr1.chunk0.sub0:0x002d` cc=0 speaker=- text=2: 請不要擔心，有那麼一天找到普萊斯特·約翰國後，一定回來的．
- `Snr1.chunk0.sub0:0x0036` cc=31 speaker=老水手洛克 text=3: 太太，這是$s家人的呀！
- `Snr1.chunk0.sub0:0x003f` cc=31 speaker=老水手洛克 text=4: 可是，船長，我聽說公爵是跟某個貴族之間有恩怨呀．
- `Snr1.chunk0.sub0:0x0051` cc=31 speaker=老水手洛克 text=6: 問題就在這裡，由於他的原因，公爵無法離開這個國家．
- `Snr1.chunk0.sub0:0x005a` cc=31 speaker=老水手洛克 text=7: 所以，很可能想要一個能替代他的優秀的人才．
- `Snr1.chunk0.sub0:0x006c` cc=31 speaker=老水手洛克 text=9: 當然，因為長期跟隨過公爵嘛．
- `Snr1.chunk0.sub0:0x0075` cc=31 speaker=老水手洛克 text=10: 噢，不管怎麼說，我對少爺出海是贊成的．
- `Snr1.chunk0.sub0:0x007e` cc=31 speaker=老水手洛克 text=11: 因為沒有比航海更能鍛練男子漢的．
- `Snr1.chunk0.sub0:0x00e9` cc=0 speaker=- text=20: 知道了，我只是想跟你告別呀．
- `Snr1.chunk0.sub0:0x0102` cc=0 speaker=- text=22: 聽說父親叫我．
- `Snr1.chunk0.sub0:0x0114` cc=0 speaker=- text=24: 還行，當然只是跟以前比較說的，若和父親比試的話，只能五場贏一場吧．
- `Snr1.chunk0.sub0:0x0126` cc=0 speaker=- text=26: 大致從理論上學了一些，但沒有實際經驗，只是紙上談兵呀！
- `Snr1.chunk0.sub0:0x0138` cc=0 speaker=- text=28: 這個事嗎，由於不允許我離開里斯本，只能從書本上學了一些．
- `Snr1.chunk0.sub0:0x014a` cc=0 speaker=- text=30: 是．
- `Snr1.chunk0.sub0:0x015c` cc=0 speaker=- text=32: 那是個人的愛好，沒法在人家的面前彈奏．
- `Snr1.chunk0.sub0:0x016e` cc=0 speaker=- text=34: 請不要笑話我．

## João Opening Selector Trace

- `0x0008` sel=1 cc=6 speaker=管家麥克 text=0: 〔管家麥克〕\n$n，很對不起，公爵有令，不許您進家門．
- `0x0024` sel=1 cc=19 speaker=$s公爵夫人 text=1: 〔$s公爵夫人〕\n哎呀，$n，這事已聽你父親說了，突然要你走出家，真殘酷呀！
- `0x002d` sel=2 cc=0 speaker=- text=2: 請不要擔心，有那麼一天找到普萊斯特·約翰國後，一定回來的．
- `0x0036` sel=2 cc=31 speaker=老水手洛克 text=3: 太太，這是$s家人的呀！
- `0x003f` sel=2 cc=31 speaker=老水手洛克 text=4: 可是，船長，我聽說公爵是跟某個貴族之間有恩怨呀．
- `0x0048` sel=1 cc=19 speaker=$s公爵夫人 text=5: 是啊，聽說跟馬丁內斯侯爵意見不和．
- `0x0051` sel=2 cc=31 speaker=老水手洛克 text=6: 問題就在這裡，由於他的原因，公爵無法離開這個國家．
- `0x005a` sel=2 cc=31 speaker=老水手洛克 text=7: 所以，很可能想要一個能替代他的優秀的人才．
- `0x0063` sel=1 cc=19 speaker=$s公爵夫人 text=8: 哎呀，洛克，你雖然長相平凡，但頭腦卻很不錯呀！
- `0x006c` sel=2 cc=31 speaker=老水手洛克 text=9: 當然，因為長期跟隨過公爵嘛．
- `0x0075` sel=2 cc=31 speaker=老水手洛克 text=10: 噢，不管怎麼說，我對少爺出海是贊成的．
- `0x007e` sel=2 cc=31 speaker=老水手洛克 text=11: 因為沒有比航海更能鍛練男子漢的．
- `0x0087` sel=1 cc=19 speaker=$s公爵夫人 text=12: 好吧，我就把$n託給你了．
- `0x0090` sel=1 cc=19 speaker=$s公爵夫人 text=13: 另外，$n，聽路琪亞小姐說你現在還沒有多少航海的資金，是麼？
- `0x0099` sel=1 cc=19 speaker=$s公爵夫人 text=14: 由於事情很突然，所以沒有準備好金幣，把這個給你吧．
- `0x00a2` sel=1 cc=19 speaker=$s公爵夫人 text=15: 這是以前我跟你父親要的銀髮飾．
- `0x00ab` sel=1 cc=19 speaker=$s公爵夫人 text=16: 把它賣掉當作資金吧，但對你爸要保密．
- `0x00b4` sel=1 cc=19 speaker=$s公爵夫人 text=17: $n，一定要多加小心，上帝保佑你．
- `0x00d0` sel=1 cc=6 speaker=管家麥克 text=18: 〔管家麥克〕\n$n，很對不起，公爵有令，不讓您進家門．
- `0x00e0` sel=1 cc=6 speaker=管家麥克 text=19: 〔管家麥克〕\n$n，很對不起，公爵有令，不讓您進家門．
- `0x00e9` sel=2 cc=0 speaker=- text=20: 知道了，我只是想跟你告別呀．
- `0x00f2` sel=1 cc=6 speaker=管家麥克 text=21: 大海像瞬間即改變其表情的怪物一樣危險．$n先生，請您一定要多加小心啊．
- `0x0102` sel=2 cc=0 speaker=- text=22: 聽說父親叫我．
- `0x010b` sel=1 cc=18 speaker=$s公爵 text=23: 〔$s公爵〕\n噢，是$n啊，你現在劍術練得如何了？
- `0x0114` sel=2 cc=0 speaker=- text=24: 還行，當然只是跟以前比較說的，若和父親比試的話，只能五場贏一場吧．
- `0x011d` sel=1 cc=18 speaker=$s公爵 text=25: 是嗎，那麼航海術呢，學好啦？
- `0x0126` sel=2 cc=0 speaker=- text=26: 大致從理論上學了一些，但沒有實際經驗，只是紙上談兵呀！
- `0x012f` sel=1 cc=18 speaker=$s公爵 text=27: 是嗎，那麼對地理學呢，擅長嗎？
- `0x0138` sel=2 cc=0 speaker=- text=28: 這個事嗎，由於不允許我離開里斯本，只能從書本上學了一些．
- `0x0141` sel=1 cc=18 speaker=$s公爵 text=29: $n，不要小看書本呀．書是先人的智慧，能把你從困境中救出來．
- `0x014a` sel=2 cc=0 speaker=- text=30: 是．
- `0x0153` sel=1 cc=18 speaker=$s公爵 text=31: $n，你彈琴怎麼樣？
- `0x015c` sel=2 cc=0 speaker=- text=32: 那是個人的愛好，沒法在人家的面前彈奏．
- `0x0165` sel=1 cc=18 speaker=$s公爵 text=33: 是嗎？聽說你得到許多女孩子們的好感呀！
- `0x016e` sel=2 cc=0 speaker=- text=34: 請不要笑話我．
- `0x0177` sel=1 cc=18 speaker=$s公爵 text=35: 哈哈哈，有機會讓我聽聽吧！
- `0x0180` sel=1 cc=18 speaker=$s公爵 text=36: $n！
- `0x0189` sel=2 cc=0 speaker=- text=37: 是．
- `0x0192` sel=1 cc=18 speaker=$s公爵 text=38: 今天有事告訴你．
- `0x019b` sel=2 cc=0 speaker=- text=39: 是什麼事啊？
- `0x01a4` sel=1 cc=18 speaker=$s公爵 text=40: 你也知道吧，當我在你那個年齡時，已率領艦隊去討伐海盜了．
- `0x01ad` sel=2 cc=0 speaker=- text=41: 是，我明白．
- `0x01b6` sel=1 cc=18 speaker=$s公爵 text=42: 過去，不允許你從這個港口出航，是因為我擔心你不成熟，容易出事．
- `0x01bf` sel=1 cc=18 speaker=$s公爵 text=43: 可是$s家族的人，不能老在陸地上待著．
- `0x01c8` sel=1 cc=18 speaker=$s公爵 text=44: 你已經俱備了一定的知識，下一步是在海上實際鍛鍊．
- `0x01d1` sel=1 cc=18 speaker=$s公爵 text=45: 這次派你去探險是葡萄牙首相兼海軍大臣萊昂·$s下達的命令．
- `0x01da` sel=2 cc=0 speaker=- text=46: 是．
- `0x01e3` sel=1 cc=18 speaker=$s公爵 text=47: 去找出叫普萊斯特·約翰的國，也許你覺得這對你過於嚴厲．但是，除非你找到普萊斯特·約翰國，不然不許回家．
- `0x01ec` sel=1 cc=18 speaker=$s公爵 text=48: 另外，我要發出公告，讓全城的人把你當作平民對待，你要有心理準備．
- `0x01f5` sel=1 cc=18 speaker=$s公爵 text=49: 你的船已叫造船廠製造，在這期間作好出航前的準備吧．
- `0x0201` sel=1 cc=18 speaker=$s公爵 text=50: 洛克，洛克在嗎？
- `0x020a` sel=2 cc=31 speaker=老水手洛克 text=51: 〔老水手洛克〕\n我在這裡．
- `0x0213` sel=1 cc=18 speaker=$s公爵 text=52: 我任命你為$n的教官，希望你把他鍛鍊成好水手．
- `0x021c` sel=2 cc=31 speaker=老水手洛克 text=53: 知道了，船長，啊！不對，公爵閣下．
- `0x0225` sel=1 cc=18 speaker=$s公爵 text=54: 不要因為他是我的兒子而客氣，要充分讓他鍛鍊啊！
- `0x0240` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=55: $n，快回公爵府吧！
- `0x024d` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=56: 〔紅鯨亭女老闆卡蕾珞娃〕\n哎喲，$n，真少見呀！
- `0x0256` sel=1 cc=98 speaker=歌女路琪亞 text=57: 〔歌女路琪亞〕\n喂，我來唱歌，你彈琴給我伴奏吧！
- `0x025f` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=58: 喂，路琪亞，對公子怎能用這種口氣說話．
- `0x0268` sel=2 cc=0 speaker=- text=59: 哈哈哈，是路琪亞要我彈，我怎能不彈呀．
- `0x0274` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=60: 想起來了，$n，你家洛克先生正找您呢，聽說公爵叫您去．
- `0x027d` sel=2 cc=0 speaker=- text=61: 是嘛，那我早點回去了．
- `0x0286` sel=1 cc=98 speaker=歌女路琪亞 text=62: 嘿，要回去了．
- `0x02a3` sel=1 cc=98 speaker=歌女路琪亞 text=63: 太太要您晚上10點到12點之間去公爵府．
- `0x02b5` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=64: $n先生，到底發生什麼事啊？街坊都鬧翻天了！
- `0x02be` sel=1 cc=98 speaker=歌女路琪亞 text=65: 喂，您真要出海啊！
- `0x02c7` sel=2 cc=0 speaker=- text=66: 是啊，這是$s家的啊．
- `0x02d0` sel=2 cc=0 speaker=- text=67: 但不知資金辦得怎麼樣了．
- `0x02d9` sel=1 cc=98 speaker=歌女路琪亞 text=68: 我們去當遊吟詩人吧，去唱歌賺錢．
- `0x02e2` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=69: 路琪亞，別說瞎話了．
- `0x02eb` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=70: $n，這裡有金幣1000枚，請您一定用上它．
- `0x02f4` sel=1 cc=31 speaker=老水手洛克 text=71: 哎喲，想不到這生意不太興隆的酒館還有不少錢呢！
- `0x02fd` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=72: 我們的買賣是不太好，真有點對不起您了．
- `0x0306` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=73: $n，您收下吧．
- `0x030f` sel=2 cc=0 speaker=- text=74: 不，這錢我不能收．我沒辦法還您呀．
- `0x0318` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=75: 沒關係．說實話，這是$s公爵委託保管的錢，他要求保密．
- `0x0321` sel=1 cc=97 speaker=紅鯨亭女老闆卡蕾珞娃 text=76: 是交給您還是交給$n先生呢？
- `0x032a` sel=2 cc=0 speaker=- text=77: 是父親嗎？
- `0x0339` sel=1 cc=31 speaker=老水手洛克 text=78: 但是要作為資金，還得再弄一些．
- `0x0342` sel=1 cc=31 speaker=老水手洛克 text=79: 對了，跟太太商量一下好嗎？
- `0x034b` sel=2 cc=0 speaker=- text=80: 那辦不到，我已經不能再進家門了．
- `0x0354` sel=1 cc=98 speaker=歌女路琪亞 text=81: 沒關係，我去聯繫吧．
- `0x035d` sel=2 cc=0 speaker=- text=82: 喂，路琪亞！
- `0x0367` sel=1 cc=98 speaker=歌女路琪亞 text=83: 回來了．
- `0x0370` sel=1 cc=31 speaker=老水手洛克 text=84: 結果怎麼樣？
- `0x0379` sel=1 cc=98 speaker=歌女路琪亞 text=85: 她說要您晚上10點到12點之間去公爵府．
- `0x0382` sel=2 cc=0 speaker=- text=86: 謝謝你，路琪亞．
- `0x03d2` sel=2 cc=0 speaker=- text=91: 不，家父政務繁忙，我又沒有航海經驗．
- `0x03e7` sel=2 cc=0 speaker=- text=94: 是嗎，主教大人，那我就回家了．
- `0x0418` sel=2 cc=0 speaker=- text=98: 謝謝，那我就不客氣了．
- `0x042c` sel=2 cc=0 speaker=- text=99: 不，我不能要主教大人的錢．
- `0x0435` sel=2 cc=0 speaker=- text=100: 把這些錢捐給教會吧．
- `0x0454` sel=2 cc=0 speaker=- text=102: 不，不能給主教大人添麻煩啊．
- `0x0471` sel=2 cc=0 speaker=- text=105: 聽說主教大人找我有事．
- `0x0484` sel=2 cc=0 speaker=- text=107: 主教大人，據我所知，您是在找航海者吧？
- `0x04a5` sel=2 cc=32 speaker=恩里克神父 text=112: 〔恩里克神父〕\n是，主教大人．
- `0x04c0` sel=2 cc=0 speaker=- text=116: 什麼？要去日本！聽父親說，它在遙遠的東方，是個浮在大海上的美麗的島國．
- `0x04c9` sel=2 cc=0 speaker=- text=117: 您說的事我現在無能為力．不要說印度洋，就連伊比利我還從未離開過．
- `0x04d2` sel=2 cc=32 speaker=恩里克神父 text=118: 但那裡的人們還沒有受過神的教誨，有多少人在翹首以待我們的到來啊．
- `0x04db` sel=2 cc=32 speaker=恩里克神父 text=119: 不管怎麼說，法王廳已命令我去佈教．拜託您了，不論用多長時間都行．
- `0x04e4` sel=2 cc=32 speaker=恩里克神父 text=120: 請帶我去日本吧．
- `0x04ed` sel=2 cc=0 speaker=- text=121: 看你這麼懇切，我只好答應你了．可是說實話，不知道要多少年才能到那裡．
- `0x04f8` sel=2 cc=31 speaker=老水手洛克 text=122: 少爺，您那麼輕易就答應下來，您真有把握嗎？
- `0x0501` sel=2 cc=0 speaker=- text=123: 日本確實非常遙遠，但千里之行始於足下，只要我們努力就一定會成功的．
- `0x050a` sel=2 cc=31 speaker=老水手洛克 text=124: 您說得有理．
- `0x0541` sel=2 cc=0 speaker=- text=126: 很可能是洛克吧．
- `0x0554` sel=2 cc=31 speaker=老水手洛克 text=128: 喂，船造好了嗎？
- `0x0594` sel=1 cc=31 speaker=老水手洛克 text=135: 少爺，沒有船怎能出海呀．去造船廠看看吧．
- `0x05ae` sel=2 cc=0 speaker=- text=137: 噢，有什麼事嗎？
- `0x05bb` sel=2 cc=0 speaker=- text=138: 對了，是想找個可靠的航海者吧．
- `0x05d4` sel=1 cc=31 speaker=老水手洛克 text=139: 少爺，沒有資金就無法出航．那家酒店的老闆娘曾經照顧過公爵，找她商量一下不好嗎？
- `0x05e1` sel=1 cc=31 speaker=老水手洛克 text=140: 少爺，您想弄出海的資金吧．那家酒店的老闆娘曾經照顧過公爵，找她商量一下不好嗎？
- `0x05ee` sel=1 cc=31 speaker=老水手洛克 text=141: 少爺，資金還是不夠啊．
- `0x05fe` sel=1 cc=31 speaker=老水手洛克 text=142: 少爺，目前準備做什麼？
- `0x0607` sel=2 cc=0 speaker=- text=143: 想先遊覽一下各地的港口．
- `0x0610` sel=1 cc=31 speaker=老水手洛克 text=144: 這個主意不太高明．
- `0x0619` sel=2 cc=0 speaker=- text=145: 為什麼？
- `0x0622` sel=1 cc=31 speaker=老水手洛克 text=146: 海上航行要花巨大的費用，而我們沒有足夠的資金啊．
- `0x062b` sel=1 cc=31 speaker=老水手洛克 text=147: 飲水不必花錢買，這暫且不提，但招募水手，買糧食等都是不小的開銷呀．
- `0x0634` sel=2 cc=0 speaker=- text=148: 你是說這些錢不夠用吧．
- `0x063d` sel=1 cc=31 speaker=老水手洛克 text=149: 是的，勉強夠用一個月的．但到那時候再想辦法就太晚了．
- `0x0646` sel=1 cc=31 speaker=老水手洛克 text=150: 遊覽各地港口，我贊成．
- `0x064f` sel=1 cc=32 speaker=恩里克神父 text=151: 洛克先生的意思是在沿途做生意吧？
- `0x0658` sel=1 cc=31 speaker=老水手洛克 text=152: 對對對，是這個意思．
- `0x0661` sel=2 cc=0 speaker=- text=153: 如果做生意，我們做什麼買賣呢？
- `0x066a` sel=1 cc=32 speaker=恩里克神父 text=154: 要是在里斯本的話，應該買它的特產岩鹽．
- `0x0673` sel=2 cc=0 speaker=- text=155: ……
- `0x067c` sel=1 cc=32 speaker=恩里克神父 text=156: 我以前在教會當過會計，對這些比較了解．
- `0x0685` sel=1 cc=32 speaker=恩里克神父 text=157: 在這個港口花大約40枚金幣買的岩鹽，能在地中海的其它港口賣到60枚以上．
- `0x069b` sel=1 cc=31 speaker=老水手洛克 text=158: 船長，看來恩里克神父精通會計，請他作我們的會計好不好？
- `0x06aa` sel=2 cc=0 speaker=- text=159: 好吧，就這麼辦．
- `0x06c8` sel=2 cc=0 speaker=- text=160: 另外，請洛克當助手．
- `0x06d9` sel=1 cc=32 speaker=恩里克神父 text=161: 對了，我還記得些以前靠過的港口的物價．
- `0x06e2` sel=1 cc=32 speaker=恩里克神父 text=162: 你通過積載一覽表，可以知道你的貨物在哪賣得最好．
- `0x06ef` sel=2 cc=0 speaker=- text=163: 不，不好意思讓神父做這種工作．
- `0x06f8` sel=1 cc=32 speaker=恩里克神父 text=164: 不，我不在乎．
- `0x0701` sel=2 cc=0 speaker=- text=165: 那，以後再拜託您吧．
- `0x0710` sel=1 cc=31 speaker=老水手洛克 text=166: 船長，請恩里克神父當會計，挺好的．
- `0x076d` sel=2 cc=0 speaker=- text=175: 代管的東西？
- `0x07ee` sel=2 cc=0 speaker=- text=186: 啊，是的．從今以後，把我當作一個普通航海者好了．

## Initial Interpretation

- `selector=1` and `selector=2` are nearly balanced globally, so the field is structural rather than incidental data.
- `selector=2` is strongly associated with `cc_arg=0`, but also appears for non-player actor slots such as João opening `cc=31` for Rocco.
- `selector=1` is common for explicit NPC speaker slots and one-line ambient/status prompts.
- Current safe name: `dialogue_selector`, not `speaker_side`; runtime validation is still needed before assigning UI or branch semantics.
