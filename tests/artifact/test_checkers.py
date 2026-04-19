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


from repopackage.artifact.checkers.task import TaskChecker
from repopackage.artifact.checkers.board import BoardChecker
from repopackage.artifact.checkers.design_spec import DesignSpecChecker
from repopackage.models.task import TaskModel, TaskStatus
from repopackage.models.board import BoardModel, PhaseModel
from repopackage.models.design_spec import DesignSpecModel


def test_task_checker_passes_valid_task():
    task = TaskModel(id="T-01", title="Do something", explanation="Detailed explanation here.", what_to_fix="Fix the thing.", how_to_do_it="Step by step.")
    result = TaskChecker().check(task)
    assert result.passed is True
    assert result.violations == []


def test_task_checker_fails_empty_explanation():
    task = TaskModel(id="T-01", title="Do something", explanation="", what_to_fix="Fix it.", how_to_do_it="Do it.")
    result = TaskChecker().check(task)
    assert result.passed is False
    assert any(v.field == "explanation" for v in result.violations)


def test_task_checker_fails_closed_without_sha():
    task = TaskModel(id="T-01", title="Done", explanation="Explanation.", what_to_fix="Fixed.", how_to_do_it="Did it.", status=TaskStatus.CLOSED, commit_sha=None)
    result = TaskChecker().check(task)
    assert result.passed is False
    assert any(v.field == "commit_sha" for v in result.violations)


def test_board_checker_passes_empty_board():
    board = BoardModel(phases=[], pills=[])
    result = BoardChecker().check(board)
    assert result.passed is True


def test_board_checker_detects_duplicate_task_ids():
    board = BoardModel(phases=[PhaseModel(id="1", tasks=["T-01", "T-02"]), PhaseModel(id="2", tasks=["T-01"])], pills=[])
    result = BoardChecker().check(board)
    assert result.passed is False
    assert any("T-01" in v.message for v in result.violations)


def test_design_spec_checker_passes_complete_spec():
    spec = DesignSpecModel(name="Test", layer_0="Context.", layer_1="Goal.", layer_2="Skeleton.", layer_3="Pseudocode.", layer_4="Patterns.", layer_5="Tests.")
    result = DesignSpecChecker().check(spec)
    assert result.passed is True


def test_design_spec_checker_fails_empty_layer():
    spec = DesignSpecModel(name="Test", layer_0="", layer_1="Goal.", layer_2="Skeleton.", layer_3="Pseudocode.", layer_4="Patterns.", layer_5="Tests.")
    result = DesignSpecChecker().check(spec)
    assert result.passed is False
    assert any(v.field == "layer_0" for v in result.violations)
