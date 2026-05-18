# sea2_demo / game

> A 大航海-style trading prototype built in Godot 4.
> **Data derived** from the reverse-engineering work in the parent directory.
> See [`../output/game_data/`](../output/game_data) for source JSON,
> [`../output/`](../output) for source PNG, [`../docs/`](../docs) for RE notes.

## MVP Status

This is Phase 4 of the master plan. The MVP demonstrates the core trading loop and a first story-bridge slice:

- ✅ World map background (rendered from RE'd Worldmap.lzw)
- ✅ 10 port markers placed on real-world geographic positions
- ✅ Click port → trade panel with 7-12 commodities per port
- ✅ Prices derived from `Za_dat.dat` (the RE'd per-port stat table)
- ✅ Buy / sell with gold balance
- ✅ Ship movement between ports
- ✅ Wind / current model (uses `Windcur.dat` 30×45 grid)
- ✅ Sea combat
- ✅ Random voyage events
- ✅ Save / load
- ✅ Story quest tab for bridge-node samples
- ⬜ Modern art (currently using RE'd worldmap as placeholder)

## Run

### Fast start

- Double-click [`../play.command`](../play.command) to launch the game directly.
- If that does not work, install Godot 4.4+ and open `project.godot`, then press F5.

### Controls

- Click a port marker on the map to sail there.
- Use the `剧情` tab inside a port to accept a quest or jump to the next story stop.
- `M` toggles music mute.
- `保存 / 读取 / 新局` are in the top-right row.

## Project layout

```
sea2_demo/game/
├── project.godot           Godot project config
├── scenes/
│   ├── main.tscn           Main scene: worldmap + UI + port layer
│   └── port_marker.tscn    Clickable port marker template
├── scripts/
│   ├── game_state.gd       Autoload: gold, inventory, port lookup
│   ├── main.gd             Main scene controller
│   └── port_marker.gd      Port marker click handling
├── assets/
│   ├── world/worldmap.png  From sea2_demo Worldmap.lzw RE
│   └── icon.svg            App icon
└── data/
    ├── ports.json          10 curated ports with commodities + prices
    └── story_quests.json   3 bridge-node sample quests
```

## Data Pipeline

All game balance numbers come from the RE'd KOEI data:

```
sea2_demo/output/game_data/za_dat.json       ──→  data/ports.json
sea2_demo/output/game_data/windcur_dat.json  ──→  (TODO) data/wind_grid.json
sea2_demo/output/game_data/monster_dat.json  ──→  (TODO) data/monsters.json
sea2_demo/output/contact_worldmap_v2.png     ──→  assets/world/worldmap.png
```

Port names are **guesses** — the original Chinese fan-translation's text
encoding wasn't fully cracked. Used real-world city names for plausible
positions based on the RE'd port atlas (Chip_no.dat).

## Next Steps

1. **Modern art** — replace placeholder worldmap with custom pixel art
2. **Expand story bridge content** — add more quest nodes and branching flags
3. **Combat prototype** — if needed, turn sea combat into a fuller tactical layer
4. **Event system** — make the trigger framework more data-driven and less hardcoded
