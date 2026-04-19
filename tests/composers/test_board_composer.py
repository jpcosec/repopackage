from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.composers.board import BoardComposer


def _make_task(task_id: str, phase: str = "1") -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel, id=task_id, title=f"Task {task_id}", explanation="Explanation.", what_to_fix="Fix.", how_to_do_it="Do.", phase=phase)


def test_board_composer_groups_by_phase():
    tasks = [_make_task("T-01", "1"), _make_task("T-02", "1"), _make_task("T-03", "2")]
    board_artifact = BoardComposer(tasks).compose()
    board = board_artifact.model
    assert len(board.phases) == 2
    phase_ids = [p.id for p in board.phases]
    assert "1" in phase_ids
    assert "2" in phase_ids


def test_board_composer_phase_contains_task_ids():
    tasks = [_make_task("T-01", "1"), _make_task("T-02", "1")]
    board_artifact = BoardComposer(tasks).compose()
    phase_1 = next(p for p in board_artifact.model.phases if p.id == "1")
    assert "T-01" in phase_1.tasks
    assert "T-02" in phase_1.tasks


def test_board_composer_empty_tasks():
    board_artifact = BoardComposer([]).compose()
    assert board_artifact.model.phases == []
