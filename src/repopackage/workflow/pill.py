from pathlib import Path
from typing import TYPE_CHECKING
from repopackage.cli.models.pill import PillModel

if TYPE_CHECKING:
    from repopackage.workflow.workspace import Workspace


class WorkflowPill:
    def __init__(self, model: PillModel, path: Path, workspace: "Workspace"):
        self.model = model
        self.path = path
        self.workspace = workspace

    @property
    def id(self) -> str:
        return self.model.metadata.id

    @property
    def title(self) -> str:
        return self.model.title

    @property
    def type(self) -> str:
        return self.model.metadata.type

    def save(self) -> None:
        from jinja2 import Environment, FileSystemLoader
        templates_dir = Path(__file__).parent.parent / "cli" / "templates"
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template("pill.md.jinja2")
        content = template.render(pill={
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "scope": self.model.metadata.scope,
            "language": self.model.metadata.language,
            "nature": self.model.metadata.nature,
            "why": self.model.why,
            "what": self.model.what,
        })
        self.path.write_text(content)
