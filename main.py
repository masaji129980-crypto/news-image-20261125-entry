#!/usr/bin/env python3
"""Entrypoint for the news-image-20261125 entry (Python 3.13, stdlib only).

The image is drawn at build time by draw.py and committed as entry.png.
This program only copies that committed file to the output directory, so
both grader runs write exactly the same bytes. It uses nothing but the
standard library and needs no network.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("error: copied file size differs from entry.png", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
