from pathlib import Path
from typing import List, TYPE_CHECKING
from pydantic import BaseModel
import subprocess

if TYPE_CHECKING:
    from repopackage.workflow.workspace import Workspace
    from repopackage.workflow.task import WorkflowTask


class EvalResult(BaseModel):
    passed: int = 0
    failed: int = 0
    output: str = ""
    success: bool = False


class Phase:
    def __init__(self, id: str, workspace: "Workspace"):
        self.id: str = id
        self.workspace: "Workspace" = workspace

    def tasks(self) -> List["WorkflowTask"]:
        from repopackage.workflow.task import WorkflowTask
        from repopackage.engines.parser import TaskParser
        tasks_dir = self.workspace.root / "desk" / "tasks"
        parser = TaskParser()
        result = []
        for f in sorted(tasks_dir.glob("T-*.md")):
            try:
                model = parser.parse_file(f)
                if (model.phase or "1") == self.id:
                    result.append(WorkflowTask(model, f, self.workspace))
            except Exception:
                pass
        return result

    def eval(self) -> EvalResult:
        proc = subprocess.run(
            ["python", "-m", "pytest", "tests/", "-q", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=self.workspace.root
        )
        output = proc.stdout + proc.stderr
        passed = output.count(" passed")
        failed = output.count(" failed")
        return EvalResult(
            passed=passed,
            failed=failed,
            output=output,
            success=proc.returncode == 0
        )
