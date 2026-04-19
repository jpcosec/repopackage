import re
from typing import Dict, Type, TypeVar
from repopackage.artifact.parsers.base import ArtifactParser
from repopackage.models.base import BaseArtifactModel
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel, PillMetadata

M = TypeVar("M", bound=BaseArtifactModel)


def _extract_title_line(raw: str) -> tuple[str, str]:
    match = re.match(r"^#\s+([\w-]+)\s+-\s+(.+)", raw.strip().splitlines()[0])
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return "", raw.strip().splitlines()[0].lstrip("# ").strip()


def _extract_sections(raw: str) -> Dict[str, str]:
    sections: Dict[str, str] = {}
    current = None
    lines = []
    for line in raw.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return sections


def _extract_footer(raw: str) -> Dict[str, str]:
    footer: Dict[str, str] = {}
    in_footer = False
    for line in raw.splitlines():
        if line.strip() == "---":
            in_footer = True
            continue
        if in_footer:
            match = re.match(r"\*\*(.+?):\*\*\s*(.*)", line.strip())
            if match:
                footer[match.group(1).strip()] = match.group(2).strip()
    return footer


def _parse_bullet_list(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        line = line.strip().lstrip("- ").strip("`").strip()
        if line:
            items.append(line)
    return items


def _parse_trait_tags(text: str) -> list[str]:
    return re.findall(r"\[([^\]]+)\]", text)


def _parse_key_value_bullets(text: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", line.strip())
        if match:
            result[match.group(1).strip()] = match.group(2).strip()
    return result


class MarkdownParser(ArtifactParser[M]):
    def parse(self, raw: str) -> M:
        if self.model_class is TaskModel:
            return self._parse_task(raw)  # type: ignore[return-value]
        if self.model_class is PillModel:
            return self._parse_pill(raw)  # type: ignore[return-value]
        raise NotImplementedError(f"No markdown parser for {self.model_class}")

    def _parse_task(self, raw: str) -> TaskModel:
        artifact_id, title = _extract_title_line(raw)
        sections = _extract_sections(raw)
        footer = _extract_footer(raw)
        return TaskModel(
            id=artifact_id,
            title=title,
            traits=_parse_trait_tags(sections.get("Traits (Composición)", "")),
            explanation=sections.get("Explanation", ""),
            reference=_parse_bullet_list(sections.get("Reference", "")),
            what_to_fix=sections.get("What to Fix / Implement", ""),
            how_to_do_it=sections.get("How to Do It (Suggested)", ""),
            induced_changes=sections.get("Induced Changes") or None,
            depends_on=_parse_bullet_list(sections.get("Depends On", "")),
            priority=sections.get("Priority", footer.get("Priority", "P2")).strip(),
            status=footer.get("Status", "open"),
            lifecycle=footer.get("Lifecycle", "target"),
            commit_sha=footer.get("Commit SHA") or None,
        )

    def _parse_pill(self, raw: str) -> PillModel:
        _, title = _extract_title_line(raw)
        sections = _extract_sections(raw)
        footer = _extract_footer(raw)
        meta_kv = _parse_key_value_bullets(sections.get("Metadata", ""))
        return PillModel(
            title=title,
            metadata=PillMetadata(
                id=meta_kv.get("ID", ""),
                type=meta_kv.get("Type", ""),
                scope=meta_kv.get("Scope", ""),
                language=meta_kv.get("Language", ""),
                nature=meta_kv.get("Nature", ""),
            ),
            why=sections.get("Why", ""),
            what=sections.get("What", ""),
            when=sections.get("When", ""),
            where=sections.get("Where", ""),
            how=sections.get("How", ""),
            lifecycle=footer.get("Lifecycle", "Keep"),
        )
