from typing import List, Dict
from repopackage.cli.models.task import TaskModel, TaskStatus
from jinja2 import Environment, FileSystemLoader
import re
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

class BoardWriter:
    """
    Generates the Tasks Board using Jinja2 templates.
    """
    def __init__(self, tasks: List[TaskModel]):
        self.tasks = tasks
        self.env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    def _get_type_domain(self, traits: List[str]) -> Dict[str, str]:
        t_type = "-"
        t_domain = "-"
        for trait in traits:
            clean_trait = trait.strip("[]")
            if clean_trait == "Implementación":
                t_type = "Impl"
            elif clean_trait == "Diseño":
                t_type = "Design"
            if clean_trait in ["CLI", "Schema", "System", "Engine"]:
                t_domain = clean_trait
        return {"type": t_type, "domain": t_domain}

    def _prepare_render_context(self) -> Dict:
        """Prepares the context for rendering the Jinja2 template."""
        context = {
            "active": [],
            "blocked": [],
            "completed": []
        }
        
        for t in self.tasks:
            td = self._get_type_domain(t.traits)
            task_render_data = {
                "id": t.id,
                "type": td['type'],
                "domain": td['domain'],
                "title": t.title,
                "priority": t.priority.value,
                "deps": t.depends_on if t.depends_on and t.depends_on != ["None"] else [],
                "pills": t.pills if t.pills else [],
                "phase": t.phase or "-",
                "blocker": t.depends_on,
                "commit_sha": t.commit_sha or "-"
            }
            
            if t.status in [TaskStatus.OPEN, TaskStatus.IN_PROGRESS]:
                context["active"].append(task_render_data)
            elif t.status == TaskStatus.BLOCKED:
                context["blocked"].append(task_render_data)
            elif t.status == TaskStatus.CLOSED:
                context["completed"].append(task_render_data)
                
        # Sort lists
        context["active"].sort(key=lambda x: x["id"])
        context["blocked"].sort(key=lambda x: x["id"])
        context["completed"].sort(key=lambda x: x["id"])

        return context

    def render_board(self) -> str:
        """Renders the board using the Jinja2 template."""
        template = self.env.get_template("board.md.jinja2")
        render_context = self._prepare_render_context()
        return template.render(tasks=render_context)
