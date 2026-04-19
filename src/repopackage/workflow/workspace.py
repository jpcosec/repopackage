from pathlib import Path
from typing import List, Optional, TYPE_CHECKING

from repopackage.workflow.desk import Desk
from repopackage.workflow.drawers import Drawers

if TYPE_CHECKING:
    from repopackage.workflow.phase import Phase


class Workspace:
    def __init__(self, root: Optional[Path] = None):
        self.root: Path = root or Path.cwd()
        self.desk: Desk = Desk(self)
        self.drawers: Drawers = Drawers(self)

    def phases(self) -> List["Phase"]:
        from repopackage.workflow.phase import Phase
        from repopackage.engines.parser import TaskParser
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
