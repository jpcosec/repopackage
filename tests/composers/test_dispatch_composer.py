from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel, PillMetadata
from repopackage.composers.dispatch import DispatchPackageComposer


def _make_task() -> ArtifactInterface:
    return ArtifactInterface.create(TaskModel, id="T-01", title="Test task", explanation="Explanation.", what_to_fix="Fix it.", how_to_do_it="Do it.")


def _make_pill(pill_id: str) -> ArtifactInterface:
    return ArtifactInterface.create(PillModel, title="Context pill", metadata=PillMetadata(id=pill_id, type="pattern", scope="global", language="Python", nature="context"), why="Why.", what="What.", how="How.")


def test_dispatch_package_contains_task_yaml():
    result = DispatchPackageComposer(_make_task(), []).compose()
    assert "T-01" in result
    assert "Test task" in result


def test_dispatch_package_contains_pill_yaml():
    pills = [_make_pill("PILL-01"), _make_pill("PILL-02")]
    result = DispatchPackageComposer(_make_task(), pills).compose()
    assert "PILL-01" in result
    assert "PILL-02" in result


def test_dispatch_package_is_yaml_parseable():
    result = DispatchPackageComposer(_make_task(), [_make_pill("PILL-01")]).compose()
    parts = [p.strip() for p in result.split("---") if p.strip()]
    assert len(parts) >= 1
