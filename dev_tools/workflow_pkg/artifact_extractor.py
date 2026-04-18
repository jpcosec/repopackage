"""Compatibility wrapper for artifact extraction."""

from __future__ import annotations

import argparse

from workflow_pkg.artifacts.service import ArtifactExtractionService


def extract_artifacts(source_path: str, include_text: bool = False) -> list:
    """Extract artifacts from a conversation source."""

    return ArtifactExtractionService().extract(source_path, include_text)


def plan_artifact_writes(artifacts: list, output_dir: str = "arctifacts") -> list:
    """Plan artifact writes from an artifact list."""

    from workflow_pkg.artifacts.planner import ArtifactWritePlanner

    return ArtifactWritePlanner().plan(artifacts, output_dir)


def extract_artifacts_to_directory(
    source_path: str, output_dir: str = "arctifacts", include_text: bool = False
) -> list:
    """Extract artifacts and write them to disk."""

    return ArtifactExtractionService().write(source_path, output_dir, include_text)


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the artifact CLI parser."""

    parser = argparse.ArgumentParser(description="Extract structured artifacts.")
    parser.add_argument("source")
    parser.add_argument("--output-dir", default="arctifacts")
    parser.add_argument("--include-text", action="store_true")
    return parser


def main() -> int:
    """Run the artifact extraction CLI."""

    args = build_argument_parser().parse_args()
    written = extract_artifacts_to_directory(
        args.source, args.output_dir, args.include_text
    )
    print(f"Wrote {len(written) - 1} artifacts to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
