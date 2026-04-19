"""Agent-prompt CLI command."""

from __future__ import annotations

import argparse

from talk_extractor.cli_pkg.command_types import CommandBase


class AgentPromptCommand(CommandBase):
    """Show fixed prompt and contract entrypoints."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        return None

    def run(self, _args: argparse.Namespace) -> int:
        """Run the command."""

        print("Agent semantic entrypoint")
        print("- Prompt: `talk_extractor/prompts/semantic_analysis.md`")
        print("- Contracts: `talk_extractor/semantic_contracts.md`")
        print("- Constraints: `talk_extractor/CONSTRAINTS.md`")
        print(
            "- Recommended command: `python -m talk_extractor run-semantic Talk.md --clean`"
        )
        print("- Then give the agent: `semantic_output/agent_brief.md`")
        return 0
