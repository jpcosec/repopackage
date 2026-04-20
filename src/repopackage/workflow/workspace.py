from pathlib import Path
from typing import Optional

class Workspace:
    """
    The Workspace represents the root of the project and provides 
    access to the Desk and Drawers.
    """
    def __init__(self, root: Optional[Path] = None):
        self.root: Path = root or Path.cwd()
        
    @property
    def desk_path(self) -> Path:
        return self.root / "desk"
        
    @property
    def tasks_path(self) -> Path:
        return self.desk_path / "tasks"
        
    @property
    def pills_path(self) -> Path:
        return self.desk_path / "pills"
