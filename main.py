#!/usr/bin/env python3
"""news-image-20261118 entry for zech.

Copies the pre-drawn entry.png (built by generate.py) to the output
directory make.fun expects. Standard library only, no network.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
