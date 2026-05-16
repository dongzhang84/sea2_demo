#!/usr/bin/env python3
"""Scripted DOSBox-X debugger runner for SNDT tracing.

This is the automation layer above scripts/dbg_driver.py. It talks to the
driver through /tmp/dbg_cmd and snapshots /tmp/dbg_screen.txt into timestamped
logs. The first version focuses on repeatable debugger-side setup:

- start dbg_driver.py if it is not already running
- send debugger commands
- set known SNDT-related breakpoints
- capture screen/log snapshots after each step

It deliberately does not require the user to play the game manually. Game-side
input automation can be added here once the debugger loop is stable.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DRIVER = ROOT / "scripts" / "dbg_driver.py"
OUT_DIR = ROOT / "output" / "sndt_trace"
CMD = Path("/tmp/dbg_cmd")
SCREEN = Path("/tmp/dbg_screen.txt")


DEFAULT_BREAKPOINTS = [
    # Event trigger check function documented in docs/SNDT交接文档.md.
    "19b4:b81a",
    # Suspected event script entry from the same handoff notes.
    "0000:8ebc",
]


class TraceRunner:
    def __init__(self, session_dir: Path, settle: float = 0.8) -> None:
        self.session_dir = session_dir
        self.settle = settle
        self.step = 0
        self.driver_proc: subprocess.Popen | None = None
        self.session_dir.mkdir(parents=True, exist_ok=True)

    def ensure_driver(self, start: bool) -> None:
        if CMD.exists() and SCREEN.exists():
            return
        if not start:
            raise RuntimeError(
                "dbg_driver.py does not appear to be running. "
                "Run scripts/dbg_driver.py first or pass --start-driver."
            )
        self.driver_proc = subprocess.Popen([sys.executable, str(DRIVER)], cwd=str(ROOT))
        self.wait_for_screen(timeout=20.0)

    def wait_for_screen(self, timeout: float = 10.0) -> str:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if SCREEN.exists():
                text = SCREEN.read_text(errors="replace")
                if text.strip():
                    return text
            time.sleep(0.25)
        raise TimeoutError("Timed out waiting for /tmp/dbg_screen.txt")

    def screen_digest(self) -> str:
        if not SCREEN.exists():
            return ""
        return hashlib.sha1(SCREEN.read_bytes()).hexdigest()

    def wait_for_screen_change(self, before: str, timeout: float = 5.0) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.screen_digest() != before:
                return
            time.sleep(0.2)

    def send(self, command: str, raw: bool = False) -> None:
        before = self.screen_digest()
        prefix = "RAW:" if raw else "LINE:"
        with CMD.open("a") as f:
            f.write(prefix + command + "\n")
        self.wait_for_screen_change(before)
        time.sleep(self.settle)

    def key(self, name: str) -> None:
        before = self.screen_digest()
        with CMD.open("a") as f:
            f.write(name + "\n")
        self.wait_for_screen_change(before)
        time.sleep(self.settle)

    def snapshot(self, label: str) -> Path:
        text = self.wait_for_screen()
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label)
        path = self.session_dir / f"{self.step:03d}_{safe}.txt"
        self.step += 1
        path.write_text(text)
        return path

    def set_breakpoint(self, address: str) -> Path:
        self.send(f"BP {address}")
        return self.snapshot(f"bp_{address}")

    def debugger_probe(self) -> None:
        self.snapshot("initial")
        for bp in DEFAULT_BREAKPOINTS:
            self.set_breakpoint(bp)
        # F5 is DOSBox-X debugger's run/continue key in dbg_driver.py.
        self.key("KEYF5")
        self.snapshot("after_continue")


def make_session_dir() -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUT_DIR / f"session_{stamp}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-driver",
        action="store_true",
        help="Start scripts/dbg_driver.py if /tmp debugger files do not exist.",
    )
    parser.add_argument(
        "--command",
        action="append",
        default=[],
        help="Extra debugger command to send after default breakpoints.",
    )
    parser.add_argument(
        "--no-default-breakpoints",
        action="store_true",
        help="Only send commands passed with --command.",
    )
    args = parser.parse_args()

    runner = TraceRunner(make_session_dir())
    runner.ensure_driver(start=args.start_driver)
    runner.snapshot("initial")

    if not args.no_default_breakpoints:
        for bp in DEFAULT_BREAKPOINTS:
            runner.set_breakpoint(bp)

    for command in args.command:
        runner.send(command)
        runner.snapshot(f"cmd_{command}")

    runner.key("KEYF5")
    runner.snapshot("after_continue")
    print(f"Wrote trace session: {runner.session_dir}")


if __name__ == "__main__":
    main()
