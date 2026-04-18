"""Paste-ready semantic prompt writer."""

from __future__ import annotations

from pathlib import Path


RUN_PROMPT_TEMPLATE = """Read `talk_extractor/semantic_contracts.md`, `talk_extractor/prompts/semantic_analysis.md`, and `talk_extractor/CONSTRAINTS.md` first.

Then run the semantic pass using the prepared workspace at `{semantic}`.

Primary entrypoint: `semantic_output/agent_brief.md`

Required evidence:
- `semantic_output/evidence.json`
- `semantic_output/manifest.json`
- `extracted talk/`
- `arctifacts/`

Required outputs to complete or update:
- `semantic_output/specs.md`
- `semantic_output/decisions.md`
- `semantic_output/timeline.md`
- `semantic_output/turns/`
- `semantic_output/artifacts/`
- `semantic_output/manifest.json`
"""


class RunPromptWriter:
    """Write a short prompt for another agent."""

    def write(self, destination: Path, semantic_dir: Path) -> None:
        """Write the paste-ready semantic prompt."""

        destination.write_text(
            RUN_PROMPT_TEMPLATE.format(semantic=semantic_dir), encoding="utf-8"
        )
