from repopackage.artifact.result import CheckResult, Violation


def test_check_result_passed():
    result = CheckResult(passed=True, violations=[])
    assert result.passed is True
    assert result.violations == []


def test_check_result_failed_has_violations():
    v = Violation(rule="required_field", message="explanation is empty", field="explanation")
    result = CheckResult(passed=False, violations=[v])
    assert result.passed is False
    assert len(result.violations) == 1
    assert result.violations[0].rule == "required_field"


def test_violation_optional_field():
    v = Violation(rule="dep_missing", message="T-99 not found")
    assert v.field is None
