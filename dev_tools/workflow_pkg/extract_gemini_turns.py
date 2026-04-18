"""Compatibility wrapper for turn extraction."""

from __future__ import annotations

import argparse

from workflow_pkg.common.slugs import slugify
from workflow_pkg.common.text import normalize_text
from workflow_pkg.turns.models import Turn
from workflow_pkg.turns.service import TurnExtractionService


def extract_turns(path: str) -> list[Turn]:
    """Extract turns from a conversation source."""

    return TurnExtractionService().extract(path)


def extract_file_to_directory(
    source_path: str, output_dir: str = "extracted talk"
) -> list:
    """Extract turns and write them to disk."""

    return TurnExtractionService().write(source_path, output_dir)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(description="Extract Gemini conversation turns.")
    parser.add_argument("source")
    parser.add_argument("--output-dir", default="extracted talk")
    return parser


def main() -> int:
    """Run the turn extraction CLI."""

    args = build_argument_parser().parse_args()
    written = extract_file_to_directory(args.source, args.output_dir)
    print(f"Wrote {len(written)} turn files to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
