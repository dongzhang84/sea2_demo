#!/bin/bash
# 双击此文件即可直接运行游戏（不打开编辑器）。
# Finder 里双击 → Terminal 启动游戏窗口。
cd "$(dirname "$0")"
GODOT="/Applications/Godot.app/Contents/MacOS/Godot"
if [ ! -x "$GODOT" ]; then
	echo "找不到 Godot：$GODOT"
	echo "请确认已安装 Godot 4 到 /Applications/。"
	read -r -p "按回车关闭..."
	exit 1
fi
"$GODOT" --path "$(pwd)/game"
