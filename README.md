# sea2_demo

这个仓库有两部分：

- `game/` - Godot 4 的可玩原型
- `docs/`、`output/`、`scripts/` - 逆向资料、导出数据和分析脚本

源素材不在 git 里。本地原始目录是 `/Users/dong/Projects/Koukai2/`。

## 现在最重要的东西

如果你想知道这个项目到底在做什么，直接看这三份：

- [game/README.md](game/README.md:1) - 原型游戏怎么运行
- [docs/游戏逻辑说明.md](docs/游戏逻辑说明.md:1) - 逆向出来的剧情拓扑和内容说明
- [docs/PHASE4_MVP_SPEC.md](docs/PHASE4_MVP_SPEC.md:1) - 下一步实现用的最小规格

如果你想看路线图和 tracker，打开：

- [ROADMAP.md](ROADMAP.md:1)
- [docs/TOPOLOGY_RE_PROPOSAL.md](docs/TOPOLOGY_RE_PROPOSAL.md:1)

## 这个仓库里有什么

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

## 备注

- `output/` 里很多文件是中间产物和自动生成结果。
- 顶层 README 不再放长过程日志，过程说明都集中到 `ROADMAP.md`、`docs/TOPOLOGY_RE_PROPOSAL.md` 和 `docs/游戏逻辑说明.md`。
