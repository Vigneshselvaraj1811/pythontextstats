"""Command-line interface for pythontextstats."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from . import analyze


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze English text.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("file", nargs="?", help="UTF-8 text file to analyze")
    source.add_argument("--text", help="Text to analyze directly")
    parser.add_argument("--wpm", type=float, default=200, help="Reading speed (default: 200)")
    parser.add_argument("--top", type=int, default=10, help="Number of frequent words to show")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args(argv)

    if args.top < 0:
        parser.error("--top must be zero or greater")
    if args.file:
        try:
            text = Path(args.file).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            parser.error(str(exc))
    elif args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.error("provide a file, --text, or piped input")

    try:
        result = analyze(text, wpm=args.wpm).as_dict()
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    result["word_frequencies"] = dict(
        list(result["word_frequencies"].items())[: args.top]
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            if key != "word_frequencies":
                print(f"{key.replace('_', ' ').title()}: {value}")
        if result["word_frequencies"]:
            print("Top words:")
            for word, count in result["word_frequencies"].items():
                print(f"  {word}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
