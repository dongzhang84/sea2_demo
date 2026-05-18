#!/usr/bin/env python3
"""Export a compact machine-readable topology bundle for the game logic."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "game_topology"


def build_bundle() -> dict:
    storylines = {
        "nodes": [
            {"id": "Snr1", "label": "Snr1 葡萄牙贵族少年线"},
            {"id": "Snr2", "label": "Snr2 西班牙军官复仇线"},
            {"id": "Snr3", "label": "Snr3 英格兰王命海军线"},
            {"id": "Snr4", "label": "Snr4 地理学家制图线"},
            {"id": "Snr5", "label": "Snr5 冒险 / 资助 / 寻宝线"},
            {"id": "Snr6", "label": "Snr6 贸易 / 发家 / 寻妹线"},
        ],
        "edges": [
            {"from": "Snr1", "to": "Snr5", "label": "公爵夫人 / 约翰"},
            {"from": "Snr1", "to": "Snr2", "label": "卡特琳娜 / 海上政治"},
            {"from": "Snr1", "to": "Snr4", "label": "约翰 / 日本线索"},
            {"from": "Snr2", "to": "Snr3", "label": "战争压力"},
            {"from": "Snr3", "to": "Snr2", "label": "海战扩散"},
            {"from": "Snr4", "to": "Snr5", "label": "黄金之国 / 法布利斯"},
            {"from": "Snr5", "to": "Snr6", "label": "夏洛克 / 皮耶德"},
            {"from": "Snr6", "to": "Snr5", "label": "资金 / 港口回流"},
            {"from": "Snr6", "to": "Snr4", "label": "劳拉 / 家乡线索"},
        ],
    }

    events = {
        "nodes": [
            {"id": "S1_E1", "label": "被逐出家门", "line": "Snr1", "actors": ["Mack", "Duke", "Duchess"], "locations": ["Lisbon", "DukeHouse"], "state_before": "HomeOutside", "state_after": "Funding"},
            {"id": "S1_E2", "label": "公爵府筹资", "line": "Snr1", "actors": ["Duchess", "Locke", "Lucia"], "locations": ["DukeHouse", "Tavern", "Church"], "state_before": "Funding", "state_after": "CanShip"},
            {"id": "S1_E3", "label": "造船完成", "line": "Snr1", "actors": ["Locke"], "locations": ["Shipyard"], "state_before": "CanShip", "state_after": "AtSea"},
            {"id": "S1_E4", "label": "恩里克神父同行", "line": "Snr1", "actors": ["Philippe", "Enrique"], "locations": ["Church", "Port"], "state_before": "AtSea", "state_after": "FarEast"},
            {"id": "S1_E5", "label": "约翰传闻", "line": "Snr1", "actors": ["John"], "locations": ["Port", "Tavern"], "state_before": "FarEast", "state_after": "InfoLoop"},
            {"id": "S1_E6", "label": "卡特琳娜卷入", "line": "Snr1", "actors": ["Catalina"], "locations": ["Port", "Sea"], "state_before": "InfoLoop", "state_after": "Revenge"},
            {"id": "S2_E1", "label": "哥哥失踪", "line": "Snr2", "actors": ["Sando"], "locations": ["Command"], "state_before": "HomeOutside", "state_after": "Revenge"},
            {"id": "S2_E2", "label": "调查真相", "line": "Snr2", "actors": ["Ezeg"], "locations": ["Command", "Port"], "state_before": "Revenge", "state_after": "InfoLoop"},
            {"id": "S2_E3", "label": "军方阻止", "line": "Snr2", "actors": ["Ezeg"], "locations": ["Command"], "state_before": "InfoLoop", "state_after": "Revenge"},
            {"id": "S2_E4", "label": "港口情报循环", "line": "Snr2", "actors": ["Catalina", "Sando"], "locations": ["Port", "Tavern"], "state_before": "Revenge", "state_after": "InfoLoop"},
            {"id": "S2_E5", "label": "卡特琳娜卷入", "line": "Snr2", "actors": ["Catalina"], "locations": ["Port", "Sea"], "state_before": "InfoLoop", "state_after": "Revenge"},
            {"id": "S2_E6", "label": "私掠 / 复仇", "line": "Snr2", "actors": ["Sando", "Ezeg"], "locations": ["Sea", "Command"], "state_before": "Revenge", "state_after": "Trade"},
            {"id": "S3_E1", "label": "国王召见", "line": "Snr3", "actors": ["Henry8", "Albert", "Gilbert"], "locations": ["Court"], "state_before": "HomeOutside", "state_after": "StateTask"},
            {"id": "S3_E2", "label": "私掠许可 / 资金", "line": "Snr3", "actors": ["Gilbert", "Henry8"], "locations": ["Court", "Port"], "state_before": "StateTask", "state_after": "CanShip"},
            {"id": "S3_E3", "label": "组建舰队", "line": "Snr3", "actors": ["HenryKing", "Gilbert"], "locations": ["Port"], "state_before": "CanShip", "state_after": "AtSea"},
            {"id": "S3_E4", "label": "对抗西班牙", "line": "Snr3", "actors": ["Carlos"], "locations": ["Sea", "NewWorld"], "state_before": "AtSea", "state_after": "Revenge"},
            {"id": "S4_E1", "label": "梅尔卡特求助", "line": "Snr4", "actors": ["Mercator"], "locations": ["Lisbon", "DukeHouse"], "state_before": "HomeOutside", "state_after": "InfoLoop"},
            {"id": "S4_E2", "label": "世界地图计划", "line": "Snr4", "actors": ["Mercator", "Laura"], "locations": ["Shipyard", "Port"], "state_before": "InfoLoop", "state_after": "FarEast"},
            {"id": "S4_E3", "label": "劳拉找家乡", "line": "Snr4", "actors": ["Laura"], "locations": ["Sea", "Port"], "state_before": "FarEast", "state_after": "SeekSasha"},
            {"id": "S4_E4", "label": "黄海 / 日本", "line": "Snr4", "actors": ["Laura"], "locations": ["EastAsia", "Japan"], "state_before": "SeekSasha", "state_after": "FarEast"},
            {"id": "S4_E5", "label": "南美 / 黄金之国", "line": "Snr4", "actors": ["Fabrice"], "locations": ["SouthAmerica", "NewWorld"], "state_before": "FarEast", "state_after": "Treasure"},
            {"id": "S5_E1", "label": "欠债 / 无资助", "line": "Snr5", "actors": ["PiedCondi", "Radinan"], "locations": ["Lisbon", "Tavern"], "state_before": "HomeOutside", "state_after": "Funding"},
            {"id": "S5_E2", "label": "公爵夫人资助", "line": "Snr5", "actors": ["Duchess", "Cameron"], "locations": ["DukeHouse", "Lisbon"], "state_before": "Funding", "state_after": "CanShip"},
            {"id": "S5_E3", "label": "冒险报告", "line": "Snr5", "actors": ["Duchess", "Cameron"], "locations": ["Port", "Tavern"], "state_before": "CanShip", "state_after": "InfoLoop"},
            {"id": "S5_E4", "label": "金质奖章", "line": "Snr5", "actors": ["John"], "locations": ["Port", "Sea"], "state_before": "InfoLoop", "state_after": "Treasure"},
            {"id": "S5_E5", "label": "黄金之国 / 圣人手杖", "line": "Snr5", "actors": ["Fabrice", "John"], "locations": ["SouthAmerica", "NewWorld"], "state_before": "Treasure", "state_after": "WorldConfirmed"},
            {"id": "S5_E6", "label": "法布利斯 / 家族线", "line": "Snr5", "actors": ["Fabrice", "Duchess"], "locations": ["Lisbon", "DukeHouse"], "state_before": "WorldConfirmed", "state_after": "StateTask"},
            {"id": "S6_E1", "label": "穷困 / 没船", "line": "Snr6", "actors": ["Tidia"], "locations": ["Tavern", "Port"], "state_before": "HomeOutside", "state_after": "Funding"},
            {"id": "S6_E2", "label": "萨达姆帮忙", "line": "Snr6", "actors": ["Sadaam"], "locations": ["Shipyard"], "state_before": "Funding", "state_after": "CanShip"},
            {"id": "S6_E3", "label": "修船 / 借债", "line": "Snr6", "actors": ["Sherlock", "Pied"], "locations": ["Shipyard", "Port"], "state_before": "CanShip", "state_after": "Trade"},
            {"id": "S6_E4", "label": "贸易 / 投资", "line": "Snr6", "actors": ["Sherlock", "Pied", "Radinan"], "locations": ["Port", "Tavern"], "state_before": "Trade", "state_after": "Trade"},
            {"id": "S6_E5", "label": "寻找薩莎", "line": "Snr6", "actors": ["Laura", "Sasha"], "locations": ["Istanbul", "Port"], "state_before": "Trade", "state_after": "SeekSasha"},
            {"id": "S6_E6", "label": "奥斯曼任务 / 同盟港", "line": "Snr6", "actors": ["Suleiman"], "locations": ["Istanbul", "Port"], "state_before": "SeekSasha", "state_after": "StateTask"},
        ],
        "edges": [
            {"from": "S1_E1", "to": "S1_E2", "label": "筹资"},
            {"from": "S1_E2", "to": "S1_E3", "label": "造船"},
            {"from": "S1_E3", "to": "S1_E4", "label": "同行"},
            {"from": "S1_E4", "to": "S1_E5", "label": "远方目标"},
            {"from": "S1_E5", "to": "S1_E6", "label": "卷入政治"},
            {"from": "S2_E1", "to": "S2_E2", "label": "调查"},
            {"from": "S2_E2", "to": "S2_E3", "label": "受阻"},
            {"from": "S2_E3", "to": "S2_E4", "label": "情报循环"},
            {"from": "S2_E4", "to": "S2_E5", "label": "卷入"},
            {"from": "S2_E5", "to": "S2_E6", "label": "复仇"},
            {"from": "S3_E1", "to": "S3_E2", "label": "许可"},
            {"from": "S3_E2", "to": "S3_E3", "label": "组建"},
            {"from": "S3_E3", "to": "S3_E4", "label": "海战"},
            {"from": "S4_E1", "to": "S4_E2", "label": "制图"},
            {"from": "S4_E2", "to": "S4_E3", "label": "寻亲"},
            {"from": "S4_E3", "to": "S4_E4", "label": "东亚"},
            {"from": "S4_E4", "to": "S4_E5", "label": "远航"},
            {"from": "S5_E1", "to": "S5_E2", "label": "资助"},
            {"from": "S5_E2", "to": "S5_E3", "label": "报告"},
            {"from": "S5_E3", "to": "S5_E4", "label": "奖章"},
            {"from": "S5_E4", "to": "S5_E5", "label": "寻宝"},
            {"from": "S5_E5", "to": "S5_E6", "label": "确认"},
            {"from": "S6_E1", "to": "S6_E2", "label": "帮忙"},
            {"from": "S6_E2", "to": "S6_E3", "label": "修船"},
            {"from": "S6_E3", "to": "S6_E4", "label": "经营"},
            {"from": "S6_E4", "to": "S6_E5", "label": "寻人"},
            {"from": "S6_E5", "to": "S6_E6", "label": "同盟"},
            {"from": "S1_E5", "to": "S4_E1", "label": "世界线索"},
            {"from": "S4_E5", "to": "S5_E5", "label": "黄金之国"},
            {"from": "S5_E6", "to": "S6_E5", "label": "家族回流"},
            {"from": "S6_E4", "to": "S5_E1", "label": "资金回流"},
        ],
    }

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
            "storylines": storylines,
            "events": events,
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
