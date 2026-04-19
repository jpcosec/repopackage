"""Compatibility wrapper for semantic workspace preparation."""

from __future__ import annotations

import argparse

from talk_extractor.semantic.workspace_preparer import SemanticWorkspacePreparer


def prepare_semantic_workspace(
    source_path: str,
    turns_dir: str = "extracted talk",
    artifacts_dir: str = "arctifacts",
    semantic_dir: str = "semantic_output",
    include_text: bool = False,
    clean: bool = False,
) -> dict:
    """Prepare a semantic workspace for an agent pass."""

    return SemanticWorkspacePreparer().prepare(
        source_path, turns_dir, artifacts_dir, semantic_dir, include_text, clean
    )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the semantic packager CLI parser."""

    parser = argparse.ArgumentParser(
        description="Prepare a semantic analysis workspace."
    )
    parser.add_argument("source")
    parser.add_argument("--turns-dir", default="extracted talk")
    parser.add_argument("--artifacts-dir", default="arctifacts")
    parser.add_argument("--semantic-dir", default="semantic_output")
    parser.add_argument("--include-text", action="store_true")
    parser.add_argument("--clean", action="store_true")
    return parser


def main() -> int:
    """Run the semantic workspace preparation CLI."""

    return _run(build_argument_parser().parse_args())


def _run(args: argparse.Namespace) -> int:
    """Run the parsed semantic workspace command."""

    evidence = prepare_semantic_workspace(
        args.source,
        args.turns_dir,
        args.artifacts_dir,
        args.semantic_dir,
        args.include_text,
        args.clean,
    )
    print(_message(evidence))
    return 0


def _message(evidence: dict) -> str:
    """Build the completion message."""

    return f"Prepared semantic workspace at {evidence['semantic_dir']} with {len(evidence['turns'])} turns and {len(evidence['artifacts'])} artifacts"


if __name__ == "__main__":
    raise SystemExit(main())
