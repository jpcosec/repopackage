from pathlib import Path
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from repopackage.workflow.workspace import Workspace
    from repopackage.workflow.task import WorkflowTask
    from repopackage.workflow.pill import WorkflowPill


class PillCollection:
    def __init__(self, workspace: "Workspace"):
        self.workspace: "Workspace" = workspace

    def all(self) -> List["WorkflowPill"]:
        from repopackage.workflow.pill import WorkflowPill
        from repopackage.engines.parser import parse_pill_markdown
        pills_dir = self.workspace.root / "desk" / "pills"
        result = []
        if not pills_dir.exists():
            return result
        for f in sorted(pills_dir.glob("PILL-*.md")):
            try:
                model = parse_pill_markdown(f.read_text())
                result.append(WorkflowPill(model, f, self.workspace))
            except Exception:
                pass
        return result

    def inject(self, task_id: str, pill_id: str) -> None:
        from repopackage.engines.markdown_engine import MarkdownEngine
        if not task_id.startswith("T-"):
            task_id = f"T-{task_id}"
        if not pill_id.startswith("PILL-"):
            pill_id = f"PILL-{pill_id}"
        task_file = self.workspace.root / "desk" / "tasks" / f"{task_id}.md"
        if not task_file.exists():
            raise FileNotFoundError(f"Task file desk/tasks/{task_id}.md not found.")
        engine = MarkdownEngine(task_file.read_text())
        current_refs = engine.read_metadata_list("Reference")
        pill_ref = f"desk/pills/{pill_id}.md"
        if pill_ref not in current_refs:
            # Update Traits
            traits_content = engine.extract_section("Traits (Composición)") or ""
            if pill_id not in traits_content:
                clean_traits = traits_content.strip("`").strip()
                new_traits = f"{clean_traits} | [{pill_id}]".strip(" |")
                engine.update_section("Traits (Composición)", f"`[{new_traits}]`" if not new_traits.startswith("[") else f"`{new_traits}`")

            # Update Reference
            current_refs.append(pill_ref)
            formatted = [f"- `{r}`" if not r.startswith("`") else f"- {r}" for r in current_refs]
            engine.update_section("Reference", "\n".join(formatted))

            # Update Induced Changes
            current_changes = engine.extract_section("Induced Changes") or ""
            current_changes = current_changes.replace("(Completar por Executor)", "").strip()
            new_changes = current_changes + f"\n- Injected pill {pill_id}"
            engine.update_section("Induced Changes", new_changes.strip())

            task_file.write_text(engine.content)


class TaskCollection:
    def __init__(self, workspace: "Workspace"):
        self.workspace: "Workspace" = workspace

    def all(self) -> List["WorkflowTask"]:
        from repopackage.workflow.task import WorkflowTask
        from repopackage.engines.parser import TaskParser
        tasks_dir = self.workspace.root / "desk" / "tasks"
        parser = TaskParser()
        result = []
        if not tasks_dir.exists():
            return result
        for f in sorted(tasks_dir.glob("T-*.md")):
            try:
                model = parser.parse_file(f)
                result.append(WorkflowTask(model, f, self.workspace))
            except Exception:
                pass
        return result

    def get(self, task_id: str) -> "WorkflowTask":
        from repopackage.workflow.task import WorkflowTask
        from repopackage.engines.parser import TaskParser
        if not task_id.startswith("T-"):
            task_id = f"T-{task_id}"
        task_file = self.workspace.root / "desk" / "tasks" / f"{task_id}.md"
        if not task_file.exists():
            raise FileNotFoundError(f"Task {task_id} not found")
        model = TaskParser().parse_file(task_file)
        return WorkflowTask(model, task_file, self.workspace)

    def atomize(self, task_id: str) -> List["WorkflowPill"]:
        from repopackage.workflow.pill import WorkflowPill
        from repopackage.engines.markdown_engine import MarkdownEngine
        from repopackage.engines.parser import parse_pill_markdown
        from jinja2 import Environment, FileSystemLoader

        if not task_id.startswith("T-"):
            task_id = f"T-{task_id}"

        task_file = self.workspace.root / "desk" / "tasks" / f"{task_id}.md"
        if not task_file.exists():
            raise FileNotFoundError(f"Task {task_id} not found")

        engine = MarkdownEngine(task_file.read_text())
        checklist_items = engine.extract_checklist("How to Do It (Suggested)")
        if not checklist_items:
            return []

        pills_dir = self.workspace.root / "desk" / "pills"
        pills_dir.mkdir(parents=True, exist_ok=True)

        templates_dir = Path(__file__).parent.parent / "cli" / "templates"
        j2_env = Environment(loader=FileSystemLoader(templates_dir))
        template = j2_env.get_template("pill.md.jinja2")

        next_id = len(list(pills_dir.glob("PILL-*.md"))) + 1
        created_pills = []

        for item in checklist_items:
            pill_id = f"PILL-{next_id:02d}"
            pill_file = pills_dir / f"{pill_id}.md"
            content = template.render(pill={
                "id": pill_id, "title": item, "type": "logic",
                "scope": "component", "language": "Python",
                "nature": "implementation", "why": "Pendiente.", "what": "Pendiente.",
            })
            pill_file.write_text(content)
            model = parse_pill_markdown(content)
            created_pills.append(WorkflowPill(model, pill_file, self.workspace))
            next_id += 1

        # Update task file with pill references
        updated = []
        for i, item in enumerate(checklist_items):
            updated.append(f"{i+1}. [{created_pills[i].id}] - {item}")
        engine.update_section("How to Do It (Suggested)", "\n".join(updated))

        current_refs = engine.read_metadata_list("Reference")
        for p in created_pills:
            ref = f"desk/pills/{p.id}.md"
            if ref not in current_refs:
                current_refs.append(ref)
        formatted = [f"- `{r}`" if not r.startswith("`") else f"- {r}" for r in current_refs]
        engine.update_section("Reference", "\n".join(formatted))
        task_file.write_text(engine.content)

        return created_pills


class Desk:
    def __init__(self, workspace: "Workspace"):
        self.workspace: "Workspace" = workspace
        self.tasks: TaskCollection = TaskCollection(workspace)
        self.pills: PillCollection = PillCollection(workspace)

    def board_sync(self) -> None:
        from repopackage.engines.board_writer import BoardWriter
        from repopackage.engines.parser import TaskParser
        tasks_dir = self.workspace.root / "desk" / "tasks"
        board_file = self.workspace.root / "desk" / "tasks" / "Board.md"
        parser = TaskParser()
        tasks = []
        if not tasks_dir.exists():
            return
        for f in sorted(tasks_dir.glob("T-*.md")):
            try:
                tasks.append(parser.parse_file(f))
            except Exception:
                pass
        writer = BoardWriter(tasks)
        board_file.write_text(writer.render_board())
