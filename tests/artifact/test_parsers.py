import pytest
from repopackage.artifact.parsers.markdown import MarkdownParser
from repopackage.models.task import TaskModel, TaskStatus, TaskPriority
from repopackage.models.pill import PillModel


def test_markdown_parser_parses_task(sample_task_md):
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    assert model.id == "T-01"
    assert model.title == "Add BaseArtifactModel"
    assert model.status == TaskStatus.OPEN
    assert model.priority == TaskPriority.P0
    assert "src/repopackage/models/base.py" in model.reference


def test_markdown_parser_parses_task_traits(sample_task_md):
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    assert "Implementación" in model.traits


def test_markdown_parser_parses_pill(sample_pill_md):
    parser = MarkdownParser(PillModel)
    model = parser.parse(sample_pill_md)
    assert model.metadata.id == "PILL-01"
    assert model.metadata.type == "pattern"
    assert model.title == "Artifact Interface Contract"
    assert "zero-context-sufficiency" in model.why


def test_markdown_parser_pill_lifecycle(sample_pill_md):
    parser = MarkdownParser(PillModel)
    model = parser.parse(sample_pill_md)
    from repopackage.models.pill import PillLifecycle
    assert model.lifecycle == PillLifecycle.KEEP
