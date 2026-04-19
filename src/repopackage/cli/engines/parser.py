from repopackage.cli.engines.markdown_engine import MarkdownEngine
from repopackage.cli.models.task import TaskModel, TaskPriority, TaskStatus
from repopackage.cli.models.pill import PillModel, PillMetadata
import re
from pathlib import Path

def parse_task_markdown(content: str) -> TaskModel:
    engine = MarkdownEngine(content)
    sections = engine.extract_sections()
    
    # Extract ID and Title from # T-01 - Title
    title_line = engine.get_title() or ""
    task_id = "UNKNOWN"
    title = title_line
    if " - " in title_line:
        task_id, title = title_line.split(" - ", 1)
    
    # Extract footer info (Status, Lifecycle, etc)
    status = TaskStatus.OPEN
    lifecycle = "target"
    commit_sha = None
    
    footer_match = re.search(r'---\n\*\*Status:\*\*\s*(.*)\n\*\*Lifecycle:\*\*\s*(.*)\n\*\*Commit SHA:\*\*\s*(.*)', content)
    if footer_match:
        status_val = footer_match.group(1).strip().lower()
        if "open" in status_val: status = TaskStatus.OPEN
        elif "closed" in status_val: status = TaskStatus.CLOSED
        elif "in_progress" in status_val: status = TaskStatus.IN_PROGRESS
        elif "blocked" in status_val: status = TaskStatus.BLOCKED
        
        lifecycle = footer_match.group(2).strip()
        commit_sha = footer_match.group(3).strip() or None

    reference = engine.read_metadata_list("reference")
    pills = [re.search(r'PILL-\d+', ref).group(0) for ref in reference if re.search(r'PILL-\d+', ref)]
    
    # Try to find Pills section directly if not in references
    if not pills and "pills" in sections:
        pill_content = sections["pills"]
        pills = [p.strip() for p in pill_content.split(",") if "PILL-" in p]

    priority_raw = sections.get("priority", "P2").split("\n")[0].strip()
    try:
        priority = TaskPriority(priority_raw)
    except ValueError:
        priority = TaskPriority.P2

    return TaskModel(
        id=task_id,
        title=title,
        traits=engine.read_metadata_list("traits_(composición)"),
        explanation=sections.get("explanation", ""),
        reference=reference,
        what_to_fix_implement=sections.get("what_to_fix_/_implement", ""),
        how_to_do_it_suggested=sections.get("how_to_do_it_(suggested)", ""),
        induced_changes=sections.get("induced_changes"),
        depends_on=engine.read_metadata_list("depends_on"),
        priority=priority,
        status=status,
        lifecycle=lifecycle,
        commit_sha=commit_sha,
        phase=sections.get("phase"),
        pills=pills
    )

class TaskParser:
    """Class based parser for tasks."""
    def parse_file(self, path: Path) -> TaskModel:
        return parse_task_markdown(path.read_text())

def parse_pill_markdown(content: str) -> PillModel:
    engine = MarkdownEngine(content)
    sections = engine.extract_sections()
    
    title = engine.get_title() or "UNKNOWN"
    metadata_dict = engine.read_key_value_pairs("metadata")
    
    lifecycle = "Still needed? (Keep)"
    footer_match = re.search(r'---\n\*\*Lifecycle:\*\*\s*(.*)', content)
    if footer_match:
        lifecycle = footer_match.group(1).strip()

    metadata = PillMetadata(
        ID=metadata_dict.get("ID", "UNKNOWN"),
        Type=metadata_dict.get("Type", "unknown"),
        Scope=metadata_dict.get("Scope", "global"),
        Language=metadata_dict.get("Language", "Python"),
        Nature=metadata_dict.get("Nature", "implementation")
    )

    return PillModel(
        title=title,
        metadata=metadata,
        why=sections.get("why", ""),
        what=sections.get("what", ""),
        how=sections.get("how", ""),
        lifecycle=lifecycle
    )
