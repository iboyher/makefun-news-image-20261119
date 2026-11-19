#!/usr/bin/env python3
"""THE WORLD — news-image-20261119 entry (Python 3.13, stdlib only).

Copies the front-page image beside this file to /output/entry.png.
The image is built by tools/build_image.py (Pillow) from
assets/hero-shenzhen.png; this program only copies bytes, so two runs
always write identical output. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.exists(src):
        raise SystemExit("entry.png missing beside main.py; nothing to copy")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
