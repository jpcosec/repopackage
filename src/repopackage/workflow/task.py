from pathlib import Path
from typing import TYPE_CHECKING
from repopackage.models.task import TaskModel

if TYPE_CHECKING:
    from repopackage.workflow.workspace import Workspace


class WorkflowTask:
    def __init__(self, model: TaskModel, path: Path, workspace: "Workspace"):
        self.model: TaskModel = model
        self.path: Path = path
        self.workspace: "Workspace" = workspace

    @property
    def id(self) -> str:
        return self.model.id

    @property
    def title(self) -> str:
        return self.model.title

    @property
    def status(self):
        return self.model.status

    @property
    def phase(self):
        return self.model.phase

    @property
    def pills(self):
        return self.model.pills

    def save(self) -> None:
        from jinja2 import Environment, FileSystemLoader
        templates_dir = Path(__file__).parent.parent / "cli" / "templates"
        env = Environment(loader=FileSystemLoader(templates_dir))
        try:
            template = env.get_template("task.md.jinja2")
            content = template.render(task=self.model)
            self.path.write_text(content)
        except Exception:
            # fallback: write current content unchanged
            pass
