"""Agent-prompt CLI command."""

from __future__ import annotations

import argparse

from workflow_pkg.cli_pkg.command_types import CommandBase


class AgentPromptCommand(CommandBase):
    """Show fixed prompt and contract entrypoints."""

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """Configure command arguments."""

        return None

    def run(self, _args: argparse.Namespace) -> int:
        """Run the command."""

        print("Agent semantic entrypoint")
        print("- Prompt: `workflow_pkg/prompts/semantic_analysis.md`")
        print("- Contracts: `workflow_pkg/semantic_contracts.md`")
        print("- Constraints: `workflow_pkg/CONSTRAINTS.md`")
        print(
            "- Recommended command: `python -m workflow_pkg run-semantic Talk.md --clean`"
        )
        print("- Then give the agent: `semantic_output/agent_brief.md`")
        return 0
