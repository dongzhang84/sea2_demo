#!/usr/bin/env python3
"""Generate original ambient BGM for the game (Phase 4, 步骤6).

The original 大航海II BGM (D2.mml) is compiled KOEI FM-driver bytecode —
reversing it is days of work and out of scope. Per the project philosophy
(原作只做风格参考), this synthesises *new* music in a similar slow,
contemplative age-of-sail style.

Output: game/assets/audio/bgm_sea.ogg + bgm_port.ogg (seamless loops).
"""
import math
import struct
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "game" / "assets" / "audio"


def midi_hz(n: float) -> float:
    return 440.0 * 2.0 ** ((n - 69) / 12.0)


def add_note(buf: np.ndarray, start: float, dur: float, midi: float,
             amp: float, harmonics, decay: float, attack: float = 0.01):
    """Additively synthesise one note, wrapping tails for a seamless loop."""
    n = int((dur + decay * 4) * SR)
    t = np.arange(n) / SR
    env = np.where(
        t < attack, t / attack,
        np.exp(-(np.maximum(t - attack, 0.0)) / decay),
    )
    # gentle release at the sustained portion's end
    wave_ = np.zeros(n)
    for k, h_amp in harmonics:
        wave_ += h_amp * np.sin(2 * math.pi * midi_hz(midi) * k * t)
    sig = wave_ * env * amp
    i0 = int(start * SR)
    N = len(buf)
    idx = (i0 + np.arange(n)) % N
    np.add.at(buf, idx, sig)


def add_pad(buf: np.ndarray, start: float, dur: float, midi: float, amp: float):
    """Sustained chord tone with slow attack/release, for the pad layer."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    atk, rel = 0.6, 0.8
    env = np.ones(n)
    env *= np.clip(t / atk, 0, 1)
    env *= np.clip((dur - t) / rel, 0, 1)
    detune = 1.0 + 0.004 * math.sin(midi)  # subtle chorus
    sig = np.zeros(n)
    for k, h_amp in [(1, 1.0), (2, 0.35), (3, 0.15), (4, 0.07)]:
        f = midi_hz(midi) * k
        sig += h_amp * 0.5 * (np.sin(2 * math.pi * f * t)
                              + np.sin(2 * math.pi * f * detune * t))
    sig *= env * amp
    i0 = int(start * SR)
    N = len(buf)
    idx = (i0 + np.arange(n)) % N
    np.add.at(buf, idx, sig)


def render(progression, melody, bass, bpm, bars):
    """progression: list of chord note-lists (midi). melody/bass: event lists."""
    beat = 60.0 / bpm
    bar = beat * 4
    total = bar * bars
    buf = np.zeros(int(total * SR))
    # Pad — one chord per bar
    for b in range(bars):
        chord = progression[b % len(progression)]
        for m in chord:
            add_pad(buf, b * bar, bar, m, 0.16)
    # Bass — root on beats 1 and 3
    for b in range(bars):
        root = bass[b % len(bass)]
        for beat_i in (0, 2):
            add_note(buf, b * bar + beat_i * beat, beat * 1.8, root,
                     0.30, [(1, 1.0), (2, 0.25)], decay=0.5)
    # Melody — music-box pluck
    for (beat_off, midi, _d) in melody:
        add_note(buf, beat_off * beat, beat, midi, 0.26,
                 [(1, 1.0), (2, 0.5), (3, 0.22), (4, 0.1)], decay=0.55)
    # Normalise with headroom + soft limit
    buf = np.tanh(buf * 1.1)
    peak = np.max(np.abs(buf)) or 1.0
    buf = buf / peak * 0.85
    return buf


def write_ogg(buf: np.ndarray, name: str):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav_path = OUT_DIR / (name + ".wav")
    ogg_path = OUT_DIR / (name + ".ogg")
    pcm = (buf * 32767).astype("<i2")
    with wave.open(str(wav_path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libvorbis",
         "-q:a", "4", str(ogg_path)],
        check=True, capture_output=True,
    )
    wav_path.unlink()
    print(f"  {ogg_path.relative_to(ROOT)}  ({ogg_path.stat().st_size // 1024} KB, "
          f"{len(buf) / SR:.1f}s loop)")


# ── bgm_sea — A minor, i-VI-III-VII (Am F C G), slow & contemplative ──
SEA_CHORDS = [
    [57, 60, 64],   # Am
    [53, 57, 60],   # F
    [60, 64, 67],   # C
    [55, 59, 62],   # G
]
SEA_BASS = [45, 41, 48, 43]
# melody beat offsets across 8 bars (32 beats), A natural minor
SEA_MELODY = [
    (0, 76, 1), (2, 74, 1), (3, 72, 1),
    (4, 72, 1), (6, 69, 1),
    (8, 67, 1), (9, 76, 1), (11, 74, 1),
    (12, 71, 1), (14, 74, 1),
    (16, 72, 1), (18, 71, 1), (19, 69, 1),
    (20, 69, 1), (22, 65, 1),
    (24, 64, 1), (25, 67, 1), (27, 72, 1),
    (28, 71, 1), (30, 69, 1),
]

# ── bgm_port — C major, I-V-vi-IV (C G Am F), warmer, a touch livelier ──
PORT_CHORDS = [
    [60, 64, 67],   # C
    [55, 59, 62],   # G
    [57, 60, 64],   # Am
    [53, 57, 60],   # F
]
PORT_BASS = [48, 43, 45, 41]
PORT_MELODY = [
    (0, 67, 1), (2, 64, 1), (3, 67, 1),
    (4, 71, 1), (6, 74, 1),
    (8, 72, 1), (9, 69, 1), (11, 72, 1),
    (12, 69, 1), (14, 65, 1),
    (16, 72, 1), (18, 76, 1), (19, 74, 1),
    (20, 71, 1), (22, 74, 1),
    (24, 76, 1), (25, 72, 1), (27, 69, 1),
    (28, 65, 1), (30, 67, 1),
]


def main():
    print("Generating BGM...")
    sea = render(SEA_CHORDS, SEA_MELODY, SEA_BASS, bpm=66, bars=8)
    write_ogg(sea, "bgm_sea")
    port = render(PORT_CHORDS, PORT_MELODY, PORT_BASS, bpm=78, bars=8)
    write_ogg(port, "bgm_port")
    print("Done.")


if __name__ == "__main__":
    main()
