#!/usr/bin/env python3
"""
Traditional Chinese to Simplified Chinese converter.
"""

import argparse
import sys
from pathlib import Path

try:
    from opencc import OpenCC
except Exception as exc:
    OpenCC = None
    _OPENCC_IMPORT_ERROR = exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Traditional Chinese to Simplified Chinese.")
    io_group = parser.add_mutually_exclusive_group(required=False)
    io_group.add_argument("-i", "--input", help="Input file path; omit to read stdin.")
    io_group.add_argument("--in-dir", help="Input directory for batch conversion.")

    out_group = parser.add_mutually_exclusive_group(required=False)
    out_group.add_argument("-o", "--output", help="Output file path; omit to write stdout.")
    out_group.add_argument("--out-dir", help="Output directory for batch conversion.")

    parser.add_argument("--encoding", default="utf-8", help="Text encoding (default: utf-8).")
    parser.add_argument(
        "--ext",
        default=".txt",
        help="File extension filter for batch mode (default: .txt).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recurse into subdirectories in batch mode.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with failure on first error in batch mode.",
    )
    return parser.parse_args()


def read_text(path: Path, encoding: str) -> str:
    return path.read_text(encoding=encoding)


def write_text(path: Path, data: str, encoding: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding=encoding)


def convert_text(converter: OpenCC, text: str) -> str:
    return converter.convert(text)


def iter_files(root: Path, ext: str, recursive: bool):
    pattern = f"**/*{ext}" if recursive else f"*{ext}"
    for path in root.glob(pattern):
        if path.is_file():
            yield path


def main() -> int:
    args = parse_args()

    if OpenCC is None:
        print(f"ERROR: opencc import failed: {_OPENCC_IMPORT_ERROR}", file=sys.stderr)
        print("Please install: pip install opencc-python-reimplemented", file=sys.stderr)
        return 2

    if args.in_dir and not args.out_dir:
        print("ERROR: --in-dir requires --out-dir.", file=sys.stderr)
        return 2
    if args.out_dir and not args.in_dir:
        print("ERROR: --out-dir requires --in-dir.", file=sys.stderr)
        return 2

    converter = OpenCC("t2s")

    # Single file or stdin/stdout
    if args.in_dir is None:
        try:
            if args.input:
                in_path = Path(args.input)
                if not in_path.exists():
                    print(f"ERROR: input file not found: {in_path}", file=sys.stderr)
                    return 2
                if not in_path.is_file():
                    print(f"ERROR: input path is not a file: {in_path}", file=sys.stderr)
                    return 2
                text = read_text(in_path, args.encoding)
            else:
                text = sys.stdin.read()

            converted = convert_text(converter, text)

            if args.output:
                out_path = Path(args.output)
                if out_path.exists() and out_path.is_dir():
                    print(f"ERROR: output path is a directory: {out_path}", file=sys.stderr)
                    return 2
                if args.input and Path(args.input).resolve() == out_path.resolve():
                    print("ERROR: in-place conversion not supported. Use different output path.", file=sys.stderr)
                    return 2
                write_text(out_path, converted, args.encoding)
            else:
                sys.stdout.write(converted)
        except Exception as exc:
            print(f"ERROR: conversion failed: {exc}", file=sys.stderr)
            return 1
        return 0

    # Batch mode
    in_root = Path(args.in_dir).resolve()
    out_root = Path(args.out_dir).resolve()
    if not in_root.exists() or not in_root.is_dir():
        print(f"ERROR: input directory not found: {in_root}", file=sys.stderr)
        return 2

    if args.recursive and out_root.is_relative_to(in_root):
        print("ERROR: output directory cannot be inside input directory with --recursive.", file=sys.stderr)
        return 2

    failed = []
    for path in iter_files(in_root, args.ext, args.recursive):
        rel = path.relative_to(in_root)
        out_path = out_root / rel
        try:
            text = read_text(path, args.encoding)
            converted = convert_text(converter, text)
            write_text(out_path, converted, args.encoding)
        except Exception as exc:
            failed.append((path, exc))
            print(f"ERROR: failed to convert {path}: {exc}", file=sys.stderr)
            if args.strict:
                return 1

    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
