"""Command-line entry point for rot13-cli."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .core import caesar_shift


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rot13-cli",
        description="Apply ROT13 (or a generalized Caesar cipher) to text. "
        "A text-obfuscation novelty with no cryptographic security value.",
    )
    parser.add_argument("text", nargs="*", help="Text to transform (default: read from stdin)")
    parser.add_argument("--file", help="Path to read input from instead of args/stdin")
    parser.add_argument(
        "--shift",
        type=int,
        default=13,
        help="Number of alphabet positions to shift (default: 13, i.e. ROT13)",
    )
    parser.add_argument(
        "--decode",
        action="store_true",
        help="Reverse the shift (equivalent to --shift with the sign flipped)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    shift = -args.shift if args.decode else args.shift

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"rot13-cli: error: {exc}", file=sys.stderr)
            return 2
    elif args.text:
        text = " ".join(args.text) + "\n"
    else:
        text = sys.stdin.read()

    result = caesar_shift(text, shift)
    sys.stdout.write(result)
    if not result.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
