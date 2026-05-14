#!/usr/bin/env python3
"""LS11 / Ls12 KOEI decompressor.

Algorithm: adapted from tzengyuxio/kaodata (dekoei/ls11.py).
Source: https://github.com/tzengyuxio/kaodata

Format:
  bytes 0-3   : magic "LS11" or "Ls12"
  bytes 4-15  : reserved
  bytes 16-271: 256-byte custom dictionary (per file!)
  bytes 272+  : index of (compressed_size, uncompressed_size, offset)
                12-byte records, BIG ENDIAN, terminated by 4 zero bytes
  data area   : compressed parts at the offsets

Compression: variable-length prefix code over big-endian bit stream
  - Read bits until you hit a 0 bit (count = mask_len)
  - Read mask_len more bits = factor
  - code = (2^mask_len - 2) + factor
  - If code < 256: emit dictionary[code]
  - If code >= 256: next code is (length - 3), back-copy (code - 256) bytes
"""
import sys
from pathlib import Path

LS11_MAGIC = (b"LS11", b"Ls12", b"LS10")


def bits_from_bytes(data: bytes):
    """Yield bits MSB-first (big-endian)."""
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1


def get_codes(data: bytes) -> list[int]:
    """Decode the prefix-coded bit stream into dictionary indices."""
    codes = []
    bit_iter = bits_from_bytes(data)
    while True:
        # Read mask_len bits until we hit a 0
        mask_len = 0
        while True:
            try:
                bit = next(bit_iter)
            except StopIteration:
                return codes
            mask_len += 1
            if bit == 0:
                break
        # Read mask_len more bits as factor
        factor = 0
        try:
            for _ in range(mask_len):
                factor = (factor << 1) | next(bit_iter)
        except StopIteration:
            return codes
        mask = (1 << mask_len) - 2
        codes.append(mask + factor)


def recover(codes: list[int], dictionary: bytes) -> bytes:
    out = bytearray()
    delta = 0
    for code in codes:
        if delta > 0:
            nc = 3 + code
            for _ in range(nc):
                pos = len(out) - delta
                if pos < 0:
                    out.append(0)
                else:
                    out.append(out[pos])
            delta = 0
        elif code < 256:
            out.append(dictionary[code])
        else:
            delta = code - 256
    return bytes(out)


def ls11_decode_parts(data: bytes) -> list[bytes]:
    if data[:4] not in LS11_MAGIC:
        raise ValueError(f"Bad magic: {data[:4]!r}")
    dictionary = data[16:16 + 256]
    pos = 16 + 256
    infos = []
    while data[pos:pos + 4] != b"\x00\x00\x00\x00":
        compressed_size = int.from_bytes(data[pos:pos + 4], "big")
        uncompressed_size = int.from_bytes(data[pos + 4:pos + 8], "big")
        offset = int.from_bytes(data[pos + 8:pos + 12], "big")
        infos.append((compressed_size, uncompressed_size, offset))
        pos += 12

    out = []
    for compressed_size, uncompressed_size, offset in infos:
        chunk = data[offset:offset + compressed_size]
        if compressed_size == uncompressed_size:
            out.append(chunk)
        else:
            codes = get_codes(chunk)
            decoded = recover(codes, dictionary)
            out.append(decoded[:uncompressed_size])
    return out


def main():
    if len(sys.argv) != 3:
        print("Usage: ls11_decode.py <input.lzw> <output_dir>")
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)

    data = src.read_bytes()
    print(f"Decoding {src.name} ({len(data):,} bytes)")
    print(f"Magic: {data[:4]}")

    parts = ls11_decode_parts(data)
    print(f"Decoded into {len(parts)} parts")

    sizes = [len(p) for p in parts]
    print(f"Part sizes:  min={min(sizes)} max={max(sizes)} total={sum(sizes):,}")

    for i, part in enumerate(parts):
        (dst / f"part_{i:04d}_{len(part)}bytes.bin").write_bytes(part)

    print(f"\nWritten {len(parts)} parts → {dst}")


if __name__ == "__main__":
    main()
