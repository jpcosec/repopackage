from repopackage.artifact.checkers.base import ArtifactChecker
from repopackage.artifact.result import CheckResult, Violation
from repopackage.models.design_spec import DesignSpecModel


class DesignSpecChecker(ArtifactChecker[DesignSpecModel]):
    def check(self, model: DesignSpecModel) -> CheckResult:
        violations = []
        for i in range(6):
            field = f"layer_{i}"
            if not getattr(model, field, "").strip():
                violations.append(Violation(rule="empty_layer", message=f"{field} is empty", field=field))
        return CheckResult(passed=len(violations) == 0, violations=violations)
