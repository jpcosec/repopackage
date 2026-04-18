"""Task Board service logic."""

from __future__ import annotations

from pathlib import Path
from workflow_pkg.cli_pkg.task_parser import TaskParser

TASKS_DIR = Path("desk/tasks")


class TaskBoard:
    """Logic for managing the task board."""

    def load_tasks(self) -> list[dict]:
        """Load all tasks from the tasks directory."""

        tasks = []
        parser = TaskParser()
        for path in TASKS_DIR.glob("*.md"):
            if path.name == "Board.md":
                continue
            text = path.read_text(encoding="utf-8")
            data = parser.parse(text)
            tasks.append(data)
        return sorted(tasks, key=lambda x: x["ID"])
