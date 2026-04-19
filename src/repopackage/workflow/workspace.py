from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from repopackage.workflow.phase import Phase
    from repopackage.workflow.desk import Desk
    from repopackage.workflow.drawers import Drawers


class Workspace:
    def __init__(self, root: Optional[Path] = None):
        self.root = root or Path.cwd()

    @property
    def desk(self) -> "Desk":
        from repopackage.workflow.desk import Desk
        return Desk(self)

    @property
    def drawers(self) -> "Drawers":
        from repopackage.workflow.drawers import Drawers
        return Drawers(self)

    def phases(self) -> List["Phase"]:
        from repopackage.workflow.phase import Phase
        from repopackage.cli.engines.parser import TaskParser
        tasks_dir = self.root / "desk" / "tasks"
        if not tasks_dir.exists():
            return [Phase("1", self)]
        parser = TaskParser()
        phase_ids = set()
        for f in sorted(tasks_dir.glob("T-*.md")):
            try:
                task = parser.parse_file(f)
                phase_ids.add(task.phase or "1")
            except Exception:
                phase_ids.add("1")
        return [Phase(pid, self) for pid in sorted(phase_ids)]

    def last_phase(self) -> "Phase":
        phases = self.phases()
        return phases[-1] if phases else self.phase("1")

    def phase(self, phase_id: str) -> "Phase":
        from repopackage.workflow.phase import Phase
        return Phase(phase_id, self)
