"""Agent brief writer."""

from __future__ import annotations

from pathlib import Path


AGENT_BRIEF_TEMPLATE = """# Agent Brief

Use `talk_extractor/prompts/semantic_analysis.md` and `talk_extractor/semantic_contracts.md` as the operating contract.
Use `talk_extractor/CONSTRAINTS.md` as the code-structure constraint contract.

## Workspace
- Conversation source: `{source}`
- Extracted turns: `{turns}`
- Extracted artifacts: `{artifacts}`
- Semantic output target: `{semantic}`

## Required Process
1. Read `talk_extractor/semantic_contracts.md`.
2. Read `talk_extractor/prompts/semantic_analysis.md`.
3. Process turn files in `{turns}` in ascending order.
4. Use `arctifacts/index.md` plus individual artifacts as evidence.
5. Fill `semantic_output/specs.md`, `semantic_output/decisions.md`, `semantic_output/timeline.md`, `semantic_output/turns/`, and curate `semantic_output/artifacts/`.
6. Update `semantic_output/manifest.json` with the final semantic state.
"""


class AgentBriefWriter:
    """Write the semantic agent brief."""

    def write(
        self,
        destination: Path,
        source_path: Path,
        turns_dir: Path,
        artifacts_dir: Path,
        semantic_dir: Path,
    ) -> None:
        """Write the brief markdown file."""

        body = AGENT_BRIEF_TEMPLATE.format(
            source=source_path,
            turns=turns_dir,
            artifacts=artifacts_dir,
            semantic=semantic_dir,
        )
        destination.write_text(body, encoding="utf-8")
