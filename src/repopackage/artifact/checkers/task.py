from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.task import TaskModel, TaskStatus


class TaskChecker(ArtifactChecker[TaskModel]):
    def check(self, model: TaskModel) -> CheckResult:
        violations = []
        if not model.explanation.strip():
            violations.append(Violation(rule="required_field", message="explanation is empty", field="explanation"))
        if not model.what_to_fix.strip():
            violations.append(Violation(rule="required_field", message="what_to_fix is empty", field="what_to_fix"))
        if not model.how_to_do_it.strip():
            violations.append(Violation(rule="required_field", message="how_to_do_it is empty", field="how_to_do_it"))
        if model.status == TaskStatus.CLOSED and not model.commit_sha:
            violations.append(Violation(rule="closed_needs_sha", message="closed task must have commit_sha", field="commit_sha"))
        return CheckResult(passed=len(violations) == 0, violations=violations)
