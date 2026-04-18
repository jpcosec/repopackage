"""Prepare extracted turns and raw artifacts."""

from __future__ import annotations

from pathlib import Path

from talk_extractor.artifact_extractor import extract_artifacts
from talk_extractor.artifacts.planner import ArtifactWritePlanner
from talk_extractor.artifacts.writer import ArtifactWriter
from talk_extractor.extract_gemini_turns import extract_file_to_directory, extract_turns
from talk_extractor.semantic.directories import WorkspaceDirectoryManager


class ArtifactPackager:
    """Prepare extracted turns and artifact files."""

    def prepare(
        self,
        source_path: str,
        turns_dir: Path,
        artifacts_dir: Path,
        include_text: bool,
        clean: bool,
    ) -> tuple[list, list]:
        """Write turns and artifacts and return them."""

        WorkspaceDirectoryManager().prepare([turns_dir, artifacts_dir], clean)
        extract_file_to_directory(source_path, turns_dir)
        turns = extract_turns(source_path)
        artifacts = extract_artifacts(source_path, include_text)
        planned = ArtifactWritePlanner().plan(artifacts, artifacts_dir)
        ArtifactWriter().write(planned, artifacts_dir)
        return turns, planned
