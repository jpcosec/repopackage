from repopackage.models.design_spec import DesignSpecModel
from repopackage.models.module_contract import ModuleContractModel, ContractField, ValidationState
from repopackage.models.evidence import EvidenceModel


def test_design_spec_model():
    spec = DesignSpecModel(
        name="Action Backend",
        layer_0="Context collected.",
        layer_1="Build artifact system.",
        layer_2="Three packages: models, artifact, composers.",
        layer_3="ArtifactInterface[M] generic pattern.",
        layer_4="Strategy pattern for parsers and checkers.",
        layer_5="Round-trip tests for all artifact types.",
    )
    assert spec.name == "Action Backend"
    assert DesignSpecModel.__template__ == "design_spec.md.jinja2"
    assert DesignSpecModel.__format__ == "markdown"


def test_module_contract_model():
    contract = ModuleContractModel(
        module_name="artifact-interface",
        version="1.0.0",
        description="Generic R/W/Check interface.",
        inputs=[ContractField(name="path", type="Path", description="File path")],
        outputs=[ContractField(name="artifact", type="ArtifactInterface", description="Loaded artifact")],
        traits=["[Schema]", "[Python]"],
        validation=ValidationState(),
    )
    assert contract.module_name == "artifact-interface"
    assert ModuleContractModel.__template__ == "module_contract.yaml.jinja2"
    assert ModuleContractModel.__format__ == "yaml"
    assert contract.validation.unit_tests is False


def test_evidence_model():
    ev = EvidenceModel(
        task_id="T-01",
        passed=True,
        lint_ok=True,
        tests_ok=True,
        raw_log="All tests passed.",
    )
    assert ev.task_id == "T-01"
    assert ev.passed is True
    assert ev.commit_sha is None
    assert EvidenceModel.__template__ == "evidence.md.jinja2"
    assert EvidenceModel.__format__ == "markdown"
