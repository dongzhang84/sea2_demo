#!/usr/bin/env python3
"""大航海II 文本解码器。

文本编码破解结果 (2026-05-15)：
  游戏文本存 2 字节大端码 → 在 KoeiCht.txt 查 (列2=该码的十六进制) →
  取列1 原始字节 → 按 GBK 解码 → 繁体中文。
KoeiCht.txt 每行: <列1 原始2字节> TAB <列2 ASCII 十六进制> CRLF。

用法: decode_text.py <Message.dat | Snr0.mes | ...>
"""
import struct
import sys
from pathlib import Path

KOUKAI = Path("/Users/dong/Projects/Koukai2")


def load_charmap():
    raw = (KOUKAI / "KoeiCht.txt").read_bytes()
    idx2gbk = {}
    for ln in raw.split(b"\r\n"):
        if b"\t" not in ln:
            continue
        a, b = ln.split(b"\t", 1)
        try:
            idx = int(b.decode("ascii"), 16)
        except ValueError:
            continue
        idx2gbk[idx] = a            # a = 原始 GBK 字节
    return idx2gbk


_IDX2GBK = load_charmap()


def decode_string(s: bytes) -> str:
    """解一条以 0x00 结尾的游戏文本。"""
    out = []
    i = 0
    while i < len(s):
        if s[i] == 0:
            break
        if i + 1 < len(s):
            code = (s[i] << 8) | s[i + 1]
            gbk = _IDX2GBK.get(code)
            if gbk is not None:
                try:
                    out.append(gbk.decode("gbk"))
                    i += 2
                    continue
                except UnicodeDecodeError:
                    pass
        c = s[i]
        if 32 <= c < 127:
            out.append(chr(c))                 # ASCII (含 %s 占位符)
        elif c == 0x0a:
            out.append("\\n")
        else:
            out.append(f"<{c:02x}>")           # 未识别 (控制码?)
        i += 1
    return "".join(out)


def parse_offsets(d: bytes, width: int):
    """读开头的偏移表。width=2 (u16 BE) 或 4 (u32 BE)。"""
    first = struct.unpack(">H" if width == 2 else ">I", d[:width])[0]
    n = first // width
    fmt = ">H" if width == 2 else ">I"
    offs = [struct.unpack_from(fmt, d, i * width)[0] for i in range(n)]
    offs.append(len(d))
    return offs


def decode_file(path: str):
    d = Path(path).read_bytes()
    name = Path(path).name
    # Message.dat = u16 表; Snr*.mes = u32 表
    width = 2 if name.lower().startswith("message") else 4
    offs = parse_offsets(d, width)
    msgs = []
    for i in range(len(offs) - 1):
        seg = d[offs[i]:offs[i + 1]]
        msgs.append(decode_string(seg))
    return msgs


if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else str(KOUKAI / "Message.dat")
    msgs = decode_file(fn)
    print(f"{Path(fn).name}: {len(msgs)} 条")
    show = range(len(msgs)) if "--all" in sys.argv else list(range(min(40, len(msgs))))
    for i in show:
        print(f"  [{i}] {msgs[i]}")
