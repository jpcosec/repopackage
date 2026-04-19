from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.composers.evidence import EvidenceComposer


def _make_task() -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel, id="T-01", title="Task", explanation="Explanation.", what_to_fix="Fix.", how_to_do_it="Do.")


def test_evidence_composer_passed():
    ev = EvidenceComposer(_make_task(), test_log="5 passed", lint_log="All clean").compose()
    assert ev.model.task_id == "T-01"
    assert ev.model.passed is True
    assert ev.model.tests_ok is True
    assert ev.model.lint_ok is True


def test_evidence_composer_failed_tests():
    ev = EvidenceComposer(_make_task(), test_log="2 failed, 3 passed", lint_log="All clean").compose()
    assert ev.model.passed is False
    assert ev.model.tests_ok is False
    assert ev.model.lint_ok is True


def test_evidence_composer_failed_lint():
    ev = EvidenceComposer(_make_task(), test_log="5 passed", lint_log="E501 line too long").compose()
    assert ev.model.passed is False
    assert ev.model.lint_ok is False
