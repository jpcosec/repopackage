"""Materialize semantic files from prepared evidence."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from workflow_pkg.semantic.agent_brief_writer import AgentBriefWriter
from workflow_pkg.semantic.evidence_builder import EvidenceBuilder
from workflow_pkg.semantic.json_writer import JsonWriter
from workflow_pkg.semantic.manifest_builder import ManifestBuilder
from workflow_pkg.semantic.run_prompt_writer import RunPromptWriter
from workflow_pkg.semantic.scaffold_writer import SemanticScaffoldWriter


class SemanticMaterializer:
    """Write semantic scaffolds and machine-readable evidence."""

    def write(self, source_path: Path, paths: dict[str, Path], turns: list, planned: list, include_text: bool) -> dict:
        """Write semantic workspace files and return evidence."""

        builder = EvidenceBuilder()
        mapping = builder.artifact_map(planned)
        self._scaffolds(paths, turns, mapping)
        return self._payloads(source_path, paths, builder, turns, planned, include_text)

    def _scaffolds(self, paths: dict[str, Path], turns: list, mapping: dict[str, list[str]]) -> None:
        """Write markdown scaffold files."""

        writer = SemanticScaffoldWriter()
        writer.write_root(paths["semantic"], turns, mapping)
        writer.write_turns(paths["semantic_turns"], turns, mapping)

    def _payloads(self, source_path: Path, paths: dict[str, Path], builder: EvidenceBuilder, turns: list, planned: list, include_text: bool) -> dict:
        """Build JSON payloads and prompt files."""

        turns_data = self._turns_data(source_path, paths, builder, turns, planned)
        artifacts_data = builder.artifacts(planned)
        return self._write_outputs(source_path, paths, turns_data, artifacts_data, include_text)

    def _turns_data(self, source_path: Path, paths: dict[str, Path], builder: EvidenceBuilder, turns: list, planned: list) -> list:
        """Build evidence turns."""

        mapping = builder.artifact_map(planned)
        turn_dir = paths["semantic_turns"].as_posix()
        return builder.turns(source_path.name, turns, mapping, turn_dir)

    def _write_outputs(self, source_path: Path, paths: dict[str, Path], turns_data: list, artifacts_data: list, include_text: bool) -> dict:
        """Write JSON outputs and prompt files."""

        evidence = self._evidence(source_path, paths, turns_data, artifacts_data, include_text)
        JsonWriter().write(paths["semantic"] / "manifest.json", ManifestBuilder().build(source_path, turns_data, artifacts_data))
        JsonWriter().write(paths["semantic"] / "evidence.json", evidence)
        self._prompts(source_path, paths)
        return evidence

    def _evidence(self, source_path: Path, paths: dict[str, Path], turns_data: list, artifacts_data: list, include_text: bool) -> dict:
        """Build the evidence payload."""

        return {"source": source_path.name, "turns_dir": paths["turns"].as_posix(), "artifacts_dir": paths["artifacts"].as_posix(), "semantic_dir": paths["semantic"].as_posix(), "include_text": include_text, "turns": [asdict(item) for item in turns_data], "artifacts": [asdict(item) for item in artifacts_data], "contracts": "workflow_pkg/semantic_contracts.md", "prompt": "workflow_pkg/prompts/semantic_analysis.md"}

    def _prompts(self, source_path: Path, paths: dict[str, Path]) -> None:
        """Write prompt-oriented helper files."""

        AgentBriefWriter().write(paths["semantic"] / "agent_brief.md", source_path, paths["turns"], paths["artifacts"], paths["semantic"])
        RunPromptWriter().write(paths["semantic"] / "run_semantic_prompt.md", paths["semantic"])
