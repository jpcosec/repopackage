import pytest
from repopackage.models.task import TaskModel, TaskStatus, TaskPriority, TaskLifecycle


def test_task_model_defaults():
    task = TaskModel(
        id="T-01",
        title="Test task",
        explanation="Some explanation",
        what_to_fix="Fix something",
        how_to_do_it="Do it this way",
    )
    assert task.id == "T-01"
    assert task.status == TaskStatus.OPEN
    assert task.priority == TaskPriority.P2
    assert task.lifecycle == TaskLifecycle.TARGET
    assert task.pills == []
    assert task.depends_on == []
    assert task.traits == []


def test_task_model_has_template_classvar():
    assert TaskModel.__template__ == "task.md.jinja2"
    assert TaskModel.__format__ == "markdown"


def test_task_status_enum_values():
    assert TaskStatus.OPEN == "open"
    assert TaskStatus.IN_PROGRESS == "in_progress"
    assert TaskStatus.CLOSED == "closed"
    assert TaskStatus.BLOCKED == "blocked"


def test_task_priority_enum_values():
    assert TaskPriority.P0 == "P0"
    assert TaskPriority.P3 == "P3"


def test_task_lifecycle_enum_values():
    assert TaskLifecycle.TARGET == "target"
    assert TaskLifecycle.CURRENT == "current"
