#!/usr/bin/env python3
"""Export a compact machine-readable topology bundle for the game logic."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "game_topology"


def build_bundle() -> dict:
    characters = {
        "nodes": [
            {"id": "Duke", "label": "公爵", "group": "royal"},
            {"id": "Duchess", "label": "公爵夫人", "group": "royal"},
            {"id": "Locke", "label": "洛克", "group": "crew"},
            {"id": "Mack", "label": "麥克", "group": "crew"},
            {"id": "Lucia", "label": "路琪亞", "group": "crew"},
            {"id": "Cameron", "label": "凱麥隆", "group": "crew"},
            {"id": "John", "label": "约翰", "group": "hub"},
            {"id": "Catalina", "label": "卡特琳娜", "group": "sea"},
            {"id": "Mercator", "label": "梅爾卡特", "group": "knowledge"},
            {"id": "Laura", "label": "翻譯勞拉", "group": "knowledge"},
            {"id": "Fabrice", "label": "法布利斯", "group": "sea"},
            {"id": "Sherlock", "label": "夏洛克", "group": "finance"},
            {"id": "Pied", "label": "皮耶德", "group": "finance"},
            {"id": "PiedCondi", "label": "皮耶德·康迪", "group": "finance"},
            {"id": "Tidia", "label": "蒂迪亞", "group": "sea"},
            {"id": "Sadaam", "label": "薩達姆", "group": "crew"},
            {"id": "Sando", "label": "桑多", "group": "military"},
            {"id": "Gilbert", "label": "監督官吉爾伯特", "group": "military"},
            {"id": "Radinan", "label": "出納拉迪楠", "group": "finance"},
            {"id": "Philippe", "label": "菲利普主教", "group": "church"},
            {"id": "Enrique", "label": "恩里克神父", "group": "church"},
            {"id": "Ezeg", "label": "艾澤格司令", "group": "military"},
            {"id": "Albert", "label": "阿爾伯特皇太子", "group": "royal"},
            {"id": "Henry8", "label": "亨利八世", "group": "royal"},
            {"id": "Manuel", "label": "瑪努埃爾王", "group": "royal"},
            {"id": "Carlos", "label": "卡洛斯王", "group": "royal"},
            {"id": "HenryKing", "label": "亨利王", "group": "royal"},
            {"id": "Suleiman", "label": "蘇萊曼大帝", "group": "royal"},
            {"id": "Sasha", "label": "薩莎", "group": "family"},
        ],
        "edges": [
            {"from": "Duke", "to": "Mack", "label": "命令"},
            {"from": "Duke", "to": "John", "label": "目标"},
            {"from": "Duchess", "to": "Locke", "label": "资助"},
            {"from": "Duchess", "to": "Cameron", "label": "资助"},
            {"from": "Locke", "to": "John", "label": "教官"},
            {"from": "Lucia", "to": "John", "label": "生活 / 资金"},
            {"from": "Cameron", "to": "Duchess", "label": "介绍资助"},
            {"from": "Philippe", "to": "Enrique", "label": "传教"},
            {"from": "Enrique", "to": "John", "label": "同行"},
            {"from": "Sando", "to": "Ezeg", "label": "军讯"},
            {"from": "Ezeg", "to": "John", "label": "阻断"},
            {"from": "Albert", "to": "Henry8", "label": "王室中介"},
            {"from": "Henry8", "to": "Duke", "label": "国家任务"},
            {"from": "Manuel", "to": "Duke", "label": "葡萄牙背景"},
            {"from": "Carlos", "to": "Henry8", "label": "战争对手"},
            {"from": "HenryKing", "to": "Henry8", "label": "海军任务"},
            {"from": "Gilbert", "to": "Henry8", "label": "监督"},
            {"from": "Mercator", "to": "Laura", "label": "制图"},
            {"from": "Laura", "to": "Sasha", "label": "寻亲"},
            {"from": "Fabrice", "to": "John", "label": "确认"},
            {"from": "Sherlock", "to": "PiedCondi", "label": "金融"},
            {"from": "Pied", "to": "PiedCondi", "label": "商业"},
            {"from": "PiedCondi", "to": "Sherlock", "label": "借贷 / 远航"},
            {"from": "Tidia", "to": "Sadaam", "label": "情感动机"},
            {"from": "Sadaam", "to": "John", "label": "伙伴"},
            {"from": "Catalina", "to": "John", "label": "卷入"},
            {"from": "Catalina", "to": "Ezeg", "label": "卷入"},
            {"from": "Radinan", "to": "Sherlock", "label": "结算"},
            {"from": "Suleiman", "to": "Sadaam", "label": "同盟港"},
        ],
    }

    locations = {
        "nodes": [
            {"id": "Lisbon", "label": "里斯本", "group": "base"},
            {"id": "DukeHouse", "label": "公爵府", "group": "base"},
            {"id": "Church", "label": "教会", "group": "base"},
            {"id": "Tavern", "label": "酒馆", "group": "base"},
            {"id": "Shipyard", "label": "造船厂", "group": "base"},
            {"id": "Port", "label": "港口", "group": "hub"},
            {"id": "Sea", "label": "船上 / 海上", "group": "hub"},
            {"id": "Command", "label": "司令部", "group": "state"},
            {"id": "Court", "label": "宫廷", "group": "state"},
            {"id": "Japan", "label": "日本", "group": "target"},
            {"id": "EastAsia", "label": "黄海", "group": "target"},
            {"id": "SouthAmerica", "label": "南美", "group": "target"},
            {"id": "NewWorld", "label": "新大陆 / 加勒比", "group": "target"},
            {"id": "Istanbul", "label": "伊斯坦堡", "group": "target"},
            {"id": "Nile", "label": "尼罗河 / 亚历山卓", "group": "target"},
        ],
        "edges": [
            {"from": "Lisbon", "to": "DukeHouse", "label": "家门 / 资助"},
            {"from": "DukeHouse", "to": "Church", "label": "教会支援"},
            {"from": "DukeHouse", "to": "Tavern", "label": "酒馆信息"},
            {"from": "Tavern", "to": "Port", "label": "筹资 / 情报"},
            {"from": "Church", "to": "Japan", "label": "传教"},
            {"from": "Shipyard", "to": "Sea", "label": "造船"},
            {"from": "Port", "to": "Sea", "label": "出海"},
            {"from": "Port", "to": "Tavern", "label": "情报循环"},
            {"from": "Port", "to": "Command", "label": "军务"},
            {"from": "Court", "to": "Port", "label": "王命"},
            {"from": "Sea", "to": "EastAsia", "label": "东亚航路"},
            {"from": "Sea", "to": "Japan", "label": "远东目标"},
            {"from": "Sea", "to": "SouthAmerica", "label": "寻宝航路"},
            {"from": "Sea", "to": "NewWorld", "label": "战争航路"},
            {"from": "Sea", "to": "Istanbul", "label": "帝国任务"},
            {"from": "Sea", "to": "Nile", "label": "古代遗迹"},
            {"from": "EastAsia", "to": "Japan", "label": "家乡线索"},
            {"from": "SouthAmerica", "to": "NewWorld", "label": "黄金之国"},
            {"from": "Istanbul", "to": "Port", "label": "同盟港"},
            {"from": "Nile", "to": "Tavern", "label": "遗物 / 传闻"},
        ],
    }

    states = {
        "nodes": [
            {"id": "HomeOutside", "label": "家门外"},
            {"id": "Funding", "label": "筹资中"},
            {"id": "CanShip", "label": "可造船"},
            {"id": "AtSea", "label": "已出海"},
            {"id": "InfoLoop", "label": "情报循环"},
            {"id": "FarEast", "label": "远东目标"},
            {"id": "Revenge", "label": "复仇目标"},
            {"id": "Treasure", "label": "寻宝目标"},
            {"id": "Trade", "label": "贸易经营"},
            {"id": "SeekSasha", "label": "寻妹目标"},
            {"id": "WorldConfirmed", "label": "世界确认"},
            {"id": "StateTask", "label": "国家任务"},
            {"id": "PortExpand", "label": "港口扩张"},
            {"id": "FamilyRestored", "label": "家庭重建"},
        ],
        "transitions": [
            {"from": "HomeOutside", "to": "Funding", "label": "被逐出家门"},
            {"from": "Funding", "to": "CanShip", "label": "公爵府筹资 / 教会支援"},
            {"from": "CanShip", "to": "AtSea", "label": "造船完成"},
            {"from": "AtSea", "to": "InfoLoop", "label": "港口 / 酒馆 / 传闻"},
            {"from": "AtSea", "to": "FarEast", "label": "日本 / 东亚线索"},
            {"from": "AtSea", "to": "Revenge", "label": "卡特琳娜 / 军方阻止"},
            {"from": "AtSea", "to": "Treasure", "label": "黄金之国 / 圣人手杖"},
            {"from": "AtSea", "to": "Trade", "label": "修船 / 借债 / 投资"},
            {"from": "Trade", "to": "SeekSasha", "label": "薩莎"},
            {"from": "Treasure", "to": "WorldConfirmed", "label": "法布利斯确认"},
            {"from": "WorldConfirmed", "to": "StateTask", "label": "王命 / 同盟港"},
            {"from": "StateTask", "to": "PortExpand", "label": "伊斯坦堡 / 同盟港"},
            {"from": "SeekSasha", "to": "FamilyRestored", "label": "重逢 / 安家"},
        ],
    }

    return {
        "schema": "sea2_game_topology_bundle_v1",
        "source": "docs/游戏逻辑说明.md",
        "graphs": {
            "characters": characters,
            "locations": locations,
            "states": states,
        },
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bundle = build_bundle()
    out = OUT_DIR / "game_topology_bundle_v1.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
