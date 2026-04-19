import pytest
import yaml
from pathlib import Path
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel, TaskStatus
from repopackage.models.pill import PillModel
from repopackage.models.module_contract import ModuleContractModel


def test_interface_create_task():
    artifact = ArtifactInterface.create(TaskModel, id="T-02", title="New task", explanation="Do the thing.", what_to_fix="Fix it.", how_to_do_it="Steps.")
    assert artifact.model.id == "T-02"
    assert isinstance(artifact.model, TaskModel)


def test_interface_to_agent_returns_yaml():
    artifact = ArtifactInterface.create(TaskModel, id="T-01", title="Test", explanation="Explanation.", what_to_fix="Fix.", how_to_do_it="Do.")
    agent_str = artifact.to_agent()
    data = yaml.safe_load(agent_str)
    assert data["id"] == "T-01"
    assert data["title"] == "Test"


def test_interface_to_disk_roundtrip_task(tmp_path, sample_task_md):
    from repopackage.artifact.parsers.markdown import MarkdownParser
    parser = MarkdownParser(TaskModel)
    model = parser.parse(sample_task_md)
    artifact = ArtifactInterface(model=model)
    out_path = tmp_path / "T-01.md"
    artifact.to_disk(out_path)
    assert out_path.exists()
    rendered = out_path.read_text()
    assert "T-01" in rendered
    assert "Add BaseArtifactModel" in rendered


def test_interface_from_disk_task(tmp_path, sample_task_md):
    task_file = tmp_path / "T-01.md"
    task_file.write_text(sample_task_md)
    artifact = ArtifactInterface.from_disk(TaskModel, task_file)
    assert artifact.model.id == "T-01"
    assert artifact.model.status == TaskStatus.OPEN


def test_interface_check_valid_task():
    artifact = ArtifactInterface.create(TaskModel, id="T-01", title="Test", explanation="Explanation.", what_to_fix="Fix.", how_to_do_it="Do.")
    result = artifact.check()
    assert result.passed is True


def test_interface_check_invalid_task():
    artifact = ArtifactInterface.create(TaskModel, id="T-01", title="Test", explanation="", what_to_fix="Fix.", how_to_do_it="Do.")
    result = artifact.check()
    assert result.passed is False


def test_interface_from_disk_module_contract(tmp_path, sample_module_contract_yaml):
    contract_file = tmp_path / "contract.yaml"
    contract_file.write_text(sample_module_contract_yaml)
    artifact = ArtifactInterface.from_disk(ModuleContractModel, contract_file)
    assert artifact.model.module_name == "artifact-interface"
