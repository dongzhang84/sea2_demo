#!/usr/bin/env python3
"""Send scripted key sequences to the DOSBox-X game window on macOS.

This is intentionally separate from sndt_trace_runner.py:

- sndt_trace_runner.py controls the DOSBox-X debugger pty.
- dosbox_game_keys.py controls the SDL game window through AppleScript.

Running this may require macOS Accessibility permission for the terminal app.
"""
from __future__ import annotations

import argparse
import subprocess
import time


SEQUENCES: dict[str, list[str]] = {
    # Conservative primitives. The opening flow is kept as data so it can be
    # tuned from trace evidence instead of hard-coded throughout the project.
    "advance_dialog": ["space"] * 8,
    "password_enter": ["return"],
    "menu_down_enter": ["down", "return"],
}


PROCESS_NAMES = ["dosbox-x", "DOSBox-X"]


def osascript_key(key: str) -> None:
    code = key_code(key)
    errors: list[str] = []
    for process_name in PROCESS_NAMES:
        script = f'''
tell application "DOSBox-X" to activate
tell application "System Events"
  tell process "{process_name}"
    set frontmost to true
    key code {code}
  end tell
end tell
'''
        result = subprocess.run(["osascript", "-e", script], text=True, capture_output=True)
        if result.returncode == 0:
            return
        errors.append(result.stderr.strip())
    raise RuntimeError("; ".join(e for e in errors if e))


def key_code(key: str) -> int:
    codes = {
        "return": 36,
        "space": 49,
        "escape": 53,
        "left": 123,
        "right": 124,
        "down": 125,
        "up": 126,
    }
    if key not in codes:
        raise ValueError(f"Unsupported key: {key}")
    return codes[key]


def send_keys(keys: list[str], delay: float) -> None:
    for key in keys:
        osascript_key(key)
        time.sleep(delay)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sequence",
        choices=sorted(SEQUENCES),
        help="Named key sequence to send.",
    )
    parser.add_argument(
        "--key",
        action="append",
        default=[],
        help="Single key to send. Can be repeated. Supported: return/space/escape/arrows.",
    )
    parser.add_argument("--delay", type=float, default=0.25)
    args = parser.parse_args()

    keys: list[str] = []
    if args.sequence:
        keys.extend(SEQUENCES[args.sequence])
    keys.extend(args.key)
    if not keys:
        parser.error("Pass --sequence or at least one --key")
    send_keys(keys, args.delay)


if __name__ == "__main__":
    main()
