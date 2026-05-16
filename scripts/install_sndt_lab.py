#!/usr/bin/env python3
"""Install or restore the SNDT lab archive in game_dos/.

This script makes the destructive part explicit and reversible:

- install: backs up game_dos/SNRDAT.LZW, then copies the lab archive over it.
- restore: restores the latest backup.

It writes a manifest under output/sndt_lab/install_manifest.json so each run is
auditable. The script does not start or stop DOSBox-X.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GAME_DOS = ROOT / "game_dos"
LAB = ROOT / "output" / "sndt_lab"
BACKUPS = LAB / "backups"
MANIFEST = LAB / "install_manifest.json"
GAME_SNRDAT = GAME_DOS / "SNRDAT.LZW"
DEFAULT_LAB_SNRDAT = LAB / "SNRDAT_min_snr4_c0s0.LZW"


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {"installs": []}


def save_manifest(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def install(lab_archive: Path) -> None:
    if not GAME_SNRDAT.exists():
        raise FileNotFoundError(GAME_SNRDAT)
    if not lab_archive.exists():
        raise FileNotFoundError(lab_archive)

    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUPS / f"SNRDAT.original.{stamp}.LZW"
    shutil.copy2(GAME_SNRDAT, backup)
    shutil.copy2(lab_archive, GAME_SNRDAT)

    manifest = load_manifest()
    manifest["installs"].append(
        {
            "timestamp": stamp,
            "action": "install",
            "backup": str(backup.relative_to(ROOT)),
            "installed": str(lab_archive.relative_to(ROOT)),
            "target": str(GAME_SNRDAT.relative_to(ROOT)),
        }
    )
    manifest["current_backup"] = str(backup.relative_to(ROOT))
    save_manifest(manifest)
    print(f"Backed up {GAME_SNRDAT} -> {backup}")
    print(f"Installed {lab_archive} -> {GAME_SNRDAT}")


def restore() -> None:
    manifest = load_manifest()
    current = manifest.get("current_backup")
    if not current:
        raise RuntimeError("No current_backup in install manifest")
    backup = ROOT / current
    if not backup.exists():
        raise FileNotFoundError(backup)
    shutil.copy2(backup, GAME_SNRDAT)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest["installs"].append(
        {
            "timestamp": stamp,
            "action": "restore",
            "backup": str(backup.relative_to(ROOT)),
            "target": str(GAME_SNRDAT.relative_to(ROOT)),
        }
    )
    save_manifest(manifest)
    print(f"Restored {backup} -> {GAME_SNRDAT}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["install", "restore"])
    parser.add_argument(
        "--archive",
        type=Path,
        default=DEFAULT_LAB_SNRDAT,
        help="Lab SNRDAT archive to install. Defaults to the Snr4 minimal lab.",
    )
    args = parser.parse_args()
    if args.action == "install":
        archive = args.archive if args.archive.is_absolute() else ROOT / args.archive
        install(archive)
    else:
        restore()


if __name__ == "__main__":
    main()
