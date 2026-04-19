from pathlib import Path
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from repopackage.workflow.workspace import Workspace
    from repopackage.workflow.task import WorkflowTask


class DrawerSpec(BaseModel):
    id: str
    title: str
    domain: str
    path: Path
    status: str = "pending"

    class Config:
        arbitrary_types_allowed = True


class Drawers:
    def __init__(self, workspace: "Workspace"):
        self.workspace = workspace

    @property
    def _board_path(self) -> Path:
        return self.workspace.root / "drawers" / "Board.md"

    @property
    def _drawers_dir(self) -> Path:
        return self.workspace.root / "drawers"

    def list(self) -> List[DrawerSpec]:
        specs = []
        if not self._drawers_dir.exists():
            return specs
        for f in sorted(self._drawers_dir.glob("*.md")):
            if f.name == "Board.md":
                continue
            specs.append(DrawerSpec(
                id=f.stem,
                title=f.stem.replace("-", " ").title(),
                domain="unknown",
                path=f,
                status="pending"
            ))
        return specs

    def add(self, spec_path: Path, title: str, domain: str) -> DrawerSpec:
        self._drawers_dir.mkdir(parents=True, exist_ok=True)
        spec_id = f"D-{len(list(self._drawers_dir.glob('*.md'))) + 1:02d}"
        dest = self._drawers_dir / f"{spec_id}.md"
        dest.write_text(spec_path.read_text())
        spec = DrawerSpec(id=spec_id, title=title, domain=domain, path=dest)
        self._update_board(spec)
        return spec

    def promote(self, spec_id: str) -> "WorkflowTask":
        from repopackage.workflow.task import WorkflowTask
        from repopackage.models.task import TaskModel, TaskStatus, TaskPriority
        from jinja2 import Environment, FileSystemLoader

        spec_file = self._drawers_dir / f"{spec_id}.md"
        if not spec_file.exists():
            raise FileNotFoundError(f"Spec {spec_id} not found in drawers")

        tasks_dir = self.workspace.root / "desk" / "tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        next_num = len(list(tasks_dir.glob("T-*.md"))) + 1
        task_id = f"T-{next_num:02d}"

        model = TaskModel(
            id=task_id,
            title=f"Promoted from {spec_id}",
            explanation=spec_file.read_text()[:500],
            what_to_fix_implement="To be defined by Supervisor.",
            how_to_do_it_suggested="To be defined by Supervisor.",
            priority=TaskPriority.P2,
            status=TaskStatus.OPEN,
        )

        templates_dir = Path(__file__).parent.parent / "cli" / "templates"
        task_file = tasks_dir / f"{task_id}.md"
        try:
            env = Environment(loader=FileSystemLoader(templates_dir))
            template = env.get_template("task.md.jinja2")
            task_file.write_text(template.render(task=model))
        except Exception:
            task_file.write_text(f"# {task_id} - Promoted from {spec_id}\n\n**Status:** open\n")

        return WorkflowTask(model, task_file, self.workspace)

    def audit(self) -> List[str]:
        issues = []
        for spec in self.list():
            content = spec.path.read_text()
            if len(content.strip()) < 50:
                issues.append(f"{spec.id}: content too short")
        return issues

    def _update_board(self, spec: DrawerSpec) -> None:
        self._drawers_dir.mkdir(parents=True, exist_ok=True)
        if not self._board_path.exists():
            self._board_path.write_text("# Drawers Board\n\n| ID | Domain | Title | Status | Path |\n|----|--------|-------|--------|------|\n")
        content = self._board_path.read_text()
        row = f"| {spec.id} | {spec.domain} | {spec.title} | {spec.status} | {spec.path.name} |\n"
        self._board_path.write_text(content + row)
