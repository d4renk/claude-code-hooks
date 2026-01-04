#!/usr/bin/env python3
"""
Convert index.html (Traditional Chinese) to Simplified Chinese.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from opencc import OpenCC
except Exception as exc:  # pragma: no cover - runtime dependency check
    OpenCC = None
    _OPENCC_IMPORT_ERROR = exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert index.html to Simplified Chinese.")
    parser.add_argument(
        "--input",
        default="index.html",
        help="Input HTML path (default: index.html).",
    )
    parser.add_argument(
        "--output",
        default="index_cn.html",
        help="Output HTML path (default: index_cn.html).",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding (default: utf-8).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if OpenCC is None:
        print(f"ERROR: opencc import failed: {_OPENCC_IMPORT_ERROR}", file=sys.stderr)
        print("Please install: pip install opencc-python-reimplemented", file=sys.stderr)
        return 2

    in_path = Path(args.input)
    if not in_path.exists() or not in_path.is_file():
        print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
        return 2

    out_path = Path(args.output)
    if out_path.resolve() == in_path.resolve():
        print("ERROR: output path must be different from input path.", file=sys.stderr)
        return 2

    text = in_path.read_text(encoding=args.encoding)
    converter = OpenCC("t2s")
    converted = converter.convert(text)
    out_path.write_text(converted, encoding=args.encoding)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
