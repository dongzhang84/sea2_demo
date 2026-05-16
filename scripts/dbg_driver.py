#!/usr/bin/env python3
"""DOSBox-X 调试器驱动 daemon。

在 pty 里跑 dosbox-x，用 pyte 把调试器 curses 画面渲染成纯文本。
通过文件收发命令——不截屏、不发键到终端窗口。

控制文件:
  /tmp/dbg_cmd     写入命令; daemon 读后清空
                   LINE:<text>  → 发 <text>+回车
                   RAW:<text>   → 发原始字节
                   KEYUP/KEYDN/KEYF5 ... → 发特殊键
  /tmp/dbg_screen.txt  当前渲染的调试器画面 (每 0.3s 刷新)
  /tmp/dbg_raw.log     pty 原始输出

用法: dbg_driver.py    (前台/后台常驻)
"""
import os
import pty
import struct
import threading
import time
import fcntl
import termios

import pyte

CONF = "/Users/dong/Projects/sea2_demo/game_dos/dosbox-x.conf"
CMD = "/tmp/dbg_cmd"
SCREEN = "/tmp/dbg_screen.txt"
RAW = "/tmp/dbg_raw.log"
COLS, ROWS = 110, 44

KEYS = {
    "KEYUP": "\x1b[A", "KEYDN": "\x1b[B", "KEYRT": "\x1b[C", "KEYLF": "\x1b[D",
    "KEYF5": "\x1b[15~", "KEYENTER": "\r", "KEYESC": "\x1b",
    "KEYPGUP": "\x1b[5~", "KEYPGDN": "\x1b[6~",
}


def main():
    for f in (CMD, SCREEN, RAW):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass
    open(CMD, "w").close()

    screen = pyte.Screen(COLS, ROWS)
    stream = pyte.Stream(screen)
    lock = threading.Lock()

    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("dosbox-x", ["dosbox-x", "-conf", CONF, "-break-start"])
        os._exit(1)

    fcntl.ioctl(fd, termios.TIOCSWINSZ,
                struct.pack("HHHH", ROWS, COLS, 0, 0))
    raw = open(RAW, "wb")

    def reader():
        while True:
            try:
                data = os.read(fd, 8192)
            except OSError:
                break
            if not data:
                break
            raw.write(data)
            raw.flush()
            with lock:
                stream.feed(data.decode("utf-8", "replace"))
    threading.Thread(target=reader, daemon=True).start()

    def snap():
        with lock:
            lines = list(screen.display)
        with open(SCREEN, "w") as f:
            f.write("\n".join(lines))

    while True:
        snap()
        time.sleep(0.3)
        try:
            with open(CMD) as f:
                cmds = f.read()
        except FileNotFoundError:
            cmds = ""
        if not cmds.strip():
            continue
        open(CMD, "w").close()
        for line in cmds.splitlines():
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("LINE:"):
                os.write(fd, line[5:].encode() + b"\r")
            elif line.startswith("RAW:"):
                os.write(fd, line[4:].encode())
            elif line in KEYS:
                os.write(fd, KEYS[line].encode())
            time.sleep(0.6)
        time.sleep(0.8)
        snap()


if __name__ == "__main__":
    main()
