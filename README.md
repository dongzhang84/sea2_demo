# sea2_demo - 大航海时代 II 资源逆向与新原型

这个仓库现在分成两条线：

- `game/` - Godot 4 的可玩原型
- `docs/`、`output/`、`scripts/` - 逆向资料、导出数据、分析脚本和设计文档

源素材不在 git 里。本地原始目录是 `/Users/dong/Projects/Koukai2/`。

## 先看什么

如果你想快速知道这个仓库到底在做什么，先看这几份：

- [game/README.md](game/README.md:1) - 原型游戏怎么运行
- [docs/游戏逻辑说明.md](docs/游戏逻辑说明.md:1) - 逆向出来的剧情拓扑、事件和文本整理
- [docs/PHASE4_MVP_SPEC.md](docs/PHASE4_MVP_SPEC.md:1) - 下一步实现用的最小规格
- [docs/PHASE3_DESIGN_DOC.md](docs/PHASE3_DESIGN_DOC.md:1) - 从逆向结果压出来的设计稿

如果你想看路线图和 tracker，打开：

- [ROADMAP.md](ROADMAP.md:1)
- [docs/TOPOLOGY_RE_PROPOSAL.md](docs/TOPOLOGY_RE_PROPOSAL.md:1)

## 当前状态

### 原型游戏

[`game/`](game) 是 Phase 4 的 Godot 4 项目。它已经包含：

- 世界地图
- 贸易
- 航行
- 风向和洋流
- 随机事件
- 海战
- 买船
- 存档
- 中文 UI
- 原创 BGM

具体运行说明见 [game/README.md](game/README.md:1)。

### 逆向成果

已经整理出来的主要内容包括：

- 视觉资源：头像、港口图、世界图、船图、决斗 sprite、角色走路帧
- 数据表：港口、风洋流、船、海怪、人物目录
- 文本：UI、菜单、任务、六条主人公剧情文本
- 拓扑：`docs/游戏逻辑说明.md`
- 设计稿：`docs/PHASE3_DESIGN_DOC.md`
- MVP 规格：`docs/PHASE4_MVP_SPEC.md`

### 资源状态概览

| 资源 | 状态 | 输出 |
|---|---|---|
| `Kao.lzw` - 128 张头像 | 已完成 | `output/contact_kao_v4.png` |
| `Kao.lzw` - 128 个 48x48 发现物/道具 | 已完成 | `output/contact_disc_v1.png` |
| `Portchip.lzw` - 港口 tile atlas | 已完成 | `output/portchip_v2/` |
| `Portmap.lzw` - 港口地图 | 已完成 | `output/contact_portmap_v2_2x2.png` |
| `Worldmap.lzw` - 世界地图 | 已完成 | `output/contact_worldmap_v2.png` |
| `Iap1-6.lzw` / `Iae1.lzw` - 决斗 sprite | 已完成 | `output/contact_iap{1-6}_v1.png` / `contact_iae1_v1.png` |
| `Char.lzw` - 角色 walking sprite | 已完成 | `output/contact_char_v2.png` |
| `Opgraph.lzw` - 事件 CG | 仍在攻坚 | - |
| `Data1.lzw` - 船数据和船 sprite | 已完成 | `output/contact_ships.png` |
| `Message.dat` - UI / 对话文本 | 已抽出 | `output/messages.json` + `messages.txt` |
| `2.pat` - 繁体中文字模 | 已完成 | `output/fonts/2pat_first256.png` |
| 100 港口数据库 | 已完成 | `output/game_data/ports_full.json` |

## 怎么跑

### 运行原型游戏

1. 安装 Godot 4.4+
2. 打开 `game/project.godot`
3. 按 F5

或者直接双击根目录的 `play.command`。

### 重新生成资源

```bash
pip install Pillow numpy

python3 scripts/inventory_lzw.py
python3 scripts/render_kao_v4.py
python3 scripts/render_disc_v1.py
python3 scripts/render_portchip_v2.py
python3 scripts/render_portmap_v2.py
python3 scripts/render_worldmap_v2.py
```

## 目录

```text
sea2_demo/
├── game/                Godot 4 原型
├── docs/                逆向结果、拓扑、设计稿
├── output/              生成的 JSON / PNG / 报告
├── scripts/             逆向、导出、渲染脚本
├── ROADMAP.md           总路线图
├── CLAUDE.md            工具约定和格式说明
└── play.command         一键启动原型
```

## 关键参考

- [JohanLi/uncharted-waters-2-research](https://github.com/JohanLi/uncharted-waters-2-research) - tile 编码、large tileset、worldmap 后处理、决斗 UI 的重要参考
- [tzengyuxio/kaodata](https://github.com/tzengyuxio/kaodata) - LS11 解压算法参考

## 技术细节

见 [CLAUDE.md](CLAUDE.md)：

- LS11 位流规范
- 各 `.lzw` 的位图编码
- Worldmap 块编码 + 后处理 pipeline

## 备注

- `output/` 里很多文件是中间产物和自动生成结果。
- 顶层 README 负责仓库入口和现状，不再放长过程日志；过程说明集中在 `ROADMAP.md`、`docs/TOPOLOGY_RE_PROPOSAL.md` 和 `docs/游戏逻辑说明.md`。
