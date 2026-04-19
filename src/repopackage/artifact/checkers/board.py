from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.board import BoardModel


class BoardChecker(ArtifactChecker[BoardModel]):
    def check(self, model: BoardModel) -> CheckResult:
        violations = []
        seen: set[str] = set()
        for phase in model.phases:
            for task_id in phase.tasks:
                if task_id in seen:
                    violations.append(Violation(rule="duplicate_task", message=f"{task_id} appears in multiple phases", field="phases"))
                seen.add(task_id)
        return CheckResult(passed=len(violations) == 0, violations=violations)
