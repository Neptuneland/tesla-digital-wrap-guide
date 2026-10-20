"""Local PNG header preflight. No image decoding, network or dependencies."""

import argparse
import re
import struct
import sys
import zlib
from pathlib import Path


def check(path):
    try:
        with path.open("rb") as stream:
            header = stream.read(33)
        size = path.stat().st_size
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if (len(header) != 33 or header[:8] != b"\x89PNG\r\n\x1a\n"
            or header[8:16] != b"\x00\x00\x00\rIHDR"):
        print("FAIL: not a PNG with a complete first IHDR chunk")
        return 1
    crc_ok = zlib.crc32(header[12:29]) == struct.unpack(">I", header[29:33])[0]
    width, height = struct.unpack(">II", header[16:24])
    dimensions_ok = width == height and 512 <= width <= 1024
    size_ok = size <= 1_000_000
    # Conservative: count the entire filename including the extension.
    name_ok = (path.suffix.lower() == ".png" and len(path.name) <= 30
               and re.fullmatch(r"[A-Za-z0-9_ -]+", path.stem) is not None)
    checks = [
        (crc_ok, "PNG signature and IHDR checksum"),
        (dimensions_ok, f"dimensions {width} x {height}"),
        (size_ok, f"size {size} bytes (conservative 1 MB budget)"),
        (name_ok, "conservative filename check"),
    ]
    for passed, description in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {description}")
    if all(passed for passed, _ in checks):
        print("Basic preflight passed. Still inspect UV mapping and vehicle compatibility.")
        return 0
    print("Fix flagged items and check Tesla's current official requirements.")
    return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    sys.exit(check(parser.parse_args().file))
