"""Run-semantic CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase
from talk_extractor.semantic_packager import prepare_semantic_workspace


class RunSemanticCommand(CommandBase):
    """Prepare semantic scaffolding and emit next-agent pointers."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        parser.add_argument("source")
        parser.add_argument("--turns-dir", default="extracted talk")
        parser.add_argument("--artifacts-dir", default="arctifacts")
        parser.add_argument("--semantic-dir", default="semantic_output")
        parser.add_argument("--include-text", action="store_true")
        parser.add_argument("--clean", action="store_true")

    def run(self, args: argparse.Namespace) -> int:
        """Run the command."""

        evidence = prepare_semantic_workspace(
            args.source,
            args.turns_dir,
            args.artifacts_dir,
            args.semantic_dir,
            args.include_text,
            args.clean,
        )
        print(self._output(evidence))
        return 0

    def _message(self, evidence: dict) -> str:
        """Build the completion message."""

        return f"Prepared semantic workspace at {evidence['semantic_dir']} with {len(evidence['turns'])} turns and {len(evidence['artifacts'])} artifacts"

    def _output(self, evidence: dict) -> str:
        """Build the full command output."""

        return (
            self._message(evidence)
            + "\nPasteable prompt: `semantic_output/run_semantic_prompt.md`\nAgent brief: `semantic_output/agent_brief.md`"
        )
