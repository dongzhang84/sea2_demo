# Sea2 Topology Bundle Report

- schema: `sea2_game_topology_bundle_v1`
- source: `docs/游戏逻辑说明.md`
- storylines: 6
- events: 33
- characters: 29
- locations: 15
- states: 14

## Storyline Crossovers
- Snr1 -> Snr5: 公爵夫人 / 约翰
- Snr1 -> Snr2: 卡特琳娜 / 海上政治
- Snr1 -> Snr4: 约翰 / 日本线索
- Snr2 -> Snr3: 战争压力
- Snr3 -> Snr2: 海战扩散
- Snr4 -> Snr5: 黄金之国 / 法布利斯
- Snr5 -> Snr6: 夏洛克 / 皮耶德
- Snr6 -> Snr5: 资金 / 港口回流
- Snr6 -> Snr4: 劳拉 / 家乡线索

## Event Counts By Line
- Snr1: 6
- Snr2: 6
- Snr3: 4
- Snr4: 5
- Snr5: 6
- Snr6: 6

## Lookup Hotspots
### Characters
- Duchess: 5 events
- Laura: 4 events
- Catalina: 3 events
- Ezeg: 3 events
- Fabrice: 3 events
- Gilbert: 3 events
- John: 3 events
- Sando: 3 events
- Cameron: 2 events
- Henry8: 2 events
- Locke: 2 events
- Mercator: 2 events
### Locations
- Port: 17 events
- Tavern: 7 events
- Sea: 6 events
- DukeHouse: 5 events
- Lisbon: 5 events
- Command: 4 events
- Shipyard: 4 events
- NewWorld: 3 events
- Church: 2 events
- Court: 2 events
- Istanbul: 2 events
- SouthAmerica: 2 events
### States
- InfoLoop: 10 events
- CanShip: 8 events
- Revenge: 8 events
- FarEast: 6 events
- Funding: 6 events
- HomeOutside: 6 events
- Trade: 5 events
- AtSea: 4 events
- SeekSasha: 4 events
- StateTask: 4 events
- Treasure: 3 events
- WorldConfirmed: 2 events

## Event Index Preview
### Snr1
- S1_E1 被逐出家门 | actors=Mack,Duke,Duchess | locations=Lisbon,DukeHouse | HomeOutside -> Funding
- S1_E2 公爵府筹资 | actors=Duchess,Locke,Lucia | locations=DukeHouse,Tavern,Church | Funding -> CanShip
- S1_E3 造船完成 | actors=Locke | locations=Shipyard | CanShip -> AtSea
- S1_E4 恩里克神父同行 | actors=Philippe,Enrique | locations=Church,Port | AtSea -> FarEast
- S1_E5 约翰传闻 | actors=John | locations=Port,Tavern | FarEast -> InfoLoop
- S1_E6 卡特琳娜卷入 | actors=Catalina | locations=Port,Sea | InfoLoop -> Revenge
### Snr2
- S2_E1 哥哥失踪 | actors=Sando | locations=Command | HomeOutside -> Revenge
- S2_E2 调查真相 | actors=Ezeg | locations=Command,Port | Revenge -> InfoLoop
- S2_E3 军方阻止 | actors=Ezeg | locations=Command | InfoLoop -> Revenge
- S2_E4 港口情报循环 | actors=Catalina,Sando | locations=Port,Tavern | Revenge -> InfoLoop
- S2_E5 卡特琳娜卷入 | actors=Catalina | locations=Port,Sea | InfoLoop -> Revenge
- S2_E6 私掠 / 复仇 | actors=Sando,Ezeg | locations=Sea,Command | Revenge -> Trade
### Snr3
- S3_E1 国王召见 | actors=Henry8,Albert,Gilbert | locations=Court | HomeOutside -> StateTask
- S3_E2 私掠许可 / 资金 | actors=Gilbert,Henry8 | locations=Court,Port | StateTask -> CanShip
- S3_E3 组建舰队 | actors=HenryKing,Gilbert | locations=Port | CanShip -> AtSea
- S3_E4 对抗西班牙 | actors=Carlos | locations=Sea,NewWorld | AtSea -> Revenge
### Snr4
- S4_E1 梅尔卡特求助 | actors=Mercator | locations=Lisbon,DukeHouse | HomeOutside -> InfoLoop
- S4_E2 世界地图计划 | actors=Mercator,Laura | locations=Shipyard,Port | InfoLoop -> FarEast
- S4_E3 劳拉找家乡 | actors=Laura | locations=Sea,Port | FarEast -> SeekSasha
- S4_E4 黄海 / 日本 | actors=Laura | locations=EastAsia,Japan | SeekSasha -> FarEast
- S4_E5 南美 / 黄金之国 | actors=Fabrice | locations=SouthAmerica,NewWorld | FarEast -> Treasure
### Snr5
- S5_E1 欠债 / 无资助 | actors=PiedCondi,Radinan | locations=Lisbon,Tavern | HomeOutside -> Funding
- S5_E2 公爵夫人资助 | actors=Duchess,Cameron | locations=DukeHouse,Lisbon | Funding -> CanShip
- S5_E3 冒险报告 | actors=Duchess,Cameron | locations=Port,Tavern | CanShip -> InfoLoop
- S5_E4 金质奖章 | actors=John | locations=Port,Sea | InfoLoop -> Treasure
- S5_E5 黄金之国 / 圣人手杖 | actors=Fabrice,John | locations=SouthAmerica,NewWorld | Treasure -> WorldConfirmed
- S5_E6 法布利斯 / 家族线 | actors=Fabrice,Duchess | locations=Lisbon,DukeHouse | WorldConfirmed -> StateTask
### Snr6
- S6_E1 穷困 / 没船 | actors=Tidia | locations=Tavern,Port | HomeOutside -> Funding
- S6_E2 萨达姆帮忙 | actors=Sadaam | locations=Shipyard | Funding -> CanShip
- S6_E3 修船 / 借债 | actors=Sherlock,Pied | locations=Shipyard,Port | CanShip -> Trade
- S6_E4 贸易 / 投资 | actors=Sherlock,Pied,Radinan | locations=Port,Tavern | Trade -> Trade
- S6_E5 寻找薩莎 | actors=Laura,Sasha | locations=Istanbul,Port | Trade -> SeekSasha
- S6_E6 奥斯曼任务 / 同盟港 | actors=Suleiman | locations=Istanbul,Port | SeekSasha -> StateTask
