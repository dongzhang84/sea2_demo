#!/usr/bin/env python3
"""Extract dialog/UI messages from Message.dat.

Format (verified):
  - First u16 BE = offset of first message (also = offset table byte size)
  - Offset table: N × u16 BE pointing to each message's start
  - Each message: null-terminated Shift-JIS bytes, with embedded:
      \\x1bCN  — color/style codes
      %s %ld %3d %3ld — printf substitutions (player/character/number)
      half-width katakana (0xa1-0xdf, valid Shift-JIS JIS X 0201)
      proper kanji (Shift-JIS double-byte)
      control bytes (\\x01-\\x09) for line breaks, prompts, etc.

Outputs:
  - output/messages.json — list of {id, offset, raw_hex, text}
  - output/messages.txt  — pretty-printed one-per-line for human reading
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = Path('/Users/dong/Projects/Koukai2/Message.dat')
OUT_JSON = REPO / 'output' / 'messages.json'
OUT_TXT = REPO / 'output' / 'messages.txt'


def parse():
    raw = SRC.read_bytes()
    first = int.from_bytes(raw[:2], 'big')
    n = first // 2
    offsets = [int.from_bytes(raw[i * 2:(i + 1) * 2], 'big') for i in range(n)]
    messages = []
    for i, start in enumerate(offsets):
        if start >= len(raw):
            continue
        end = raw.find(b'\x00', start)
        if end < 0:
            end = len(raw)
        chunk = raw[start:end]
        try:
            text = chunk.decode('shift_jis', errors='replace')
        except Exception:
            text = '<decode error>'
        messages.append({
            'id': i,
            'offset': start,
            'len': end - start,
            'raw_hex': chunk.hex(),
            'text': text,
        })
    return messages


def pretty(text: str) -> str:
    """Make control bytes visible in the txt dump."""
    out = []
    for c in text:
        cp = ord(c)
        if cp == 0x1b:
            out.append('<ESC>')
        elif cp < 0x20:
            out.append(f'<{cp:02x}>')
        else:
            out.append(c)
    return ''.join(out)


def main():
    msgs = parse()
    OUT_JSON.parent.mkdir(exist_ok=True)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)
    print(f'→ {OUT_JSON}  {len(msgs)} messages')

    with OUT_TXT.open('w', encoding='utf-8') as f:
        for m in msgs:
            f.write(f"[{m['id']:4d}] {pretty(m['text'])}\n")
    print(f'→ {OUT_TXT}')

    # Stats
    japan_chars = sum(
        sum(1 for c in m['text'] if 0x3000 <= ord(c) <= 0x9fff)
        for m in msgs
    )
    half_kana = sum(
        sum(1 for c in m['text'] if 0xff61 <= ord(c) <= 0xff9f)
        for m in msgs
    )
    has_var = sum(1 for m in msgs if re.search(r'%[sd]|%\d*l?d', m['text']))
    has_esc = sum(1 for m in msgs if '\x1b' in m['text'])
    print(f'\nStats:')
    print(f'  total messages: {len(msgs)}')
    print(f'  full-width Japanese chars: {japan_chars:,}')
    print(f'  half-width katakana chars: {half_kana:,}')
    print(f'  messages with printf var:  {has_var}')
    print(f'  messages with ESC codes:   {has_esc}')


if __name__ == '__main__':
    main()
