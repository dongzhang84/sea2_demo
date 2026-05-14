# sea2_demo / game

> A 大航海-style trading prototype built in Godot 4.
> **Data derived** from the reverse-engineering work in the parent directory.
> See [`../output/game_data/`](../output/game_data) for source JSON,
> [`../output/`](../output) for source PNG, [`../docs/`](../docs) for RE notes.

## MVP Status

This is Phase 4 of the master plan. The MVP demonstrates the core trading loop:

- ✅ World map background (rendered from RE'd Worldmap.lzw)
- ✅ 10 port markers placed on real-world geographic positions
- ✅ Click port → trade panel with 7-12 commodities per port
- ✅ Prices derived from `Za_dat.dat` (the RE'd per-port stat table)
- ✅ Buy / sell with gold balance
- ⬜ Ship movement between ports (TODO)
- ⬜ Wind / current model (uses `Windcur.dat` 30×45 grid, TODO)
- ⬜ Sea combat (TODO)
- ⬜ Events (TODO)
- ⬜ Modern art (currently using RE'd worldmap as placeholder)

## Run

1. Install Godot 4.4+
2. Open `project.godot` in the Godot editor
3. Press F5 (Play)

## Project layout

```
sea_demo_new/
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
    └── ports.json          10 curated ports with commodities + prices
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

1. **Ship sprite + movement** — animate position between ports
2. **Wind/current overlay** — use the 30×45 grid from Windcur.dat
3. **Modern art** — replace placeholder worldmap with custom pixel art
4. **Combat prototype** — hex grid + 大航海II's wind-angle mechanics
5. **Event system** — YAML-driven trigger framework
