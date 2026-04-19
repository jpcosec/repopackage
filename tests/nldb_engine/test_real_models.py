import pytest
from repopackage.models import (
    TaskModel, PillModel, PillMetadata, BoardModel, PhaseModel, 
    EvidenceModel, DesignSpecModel, ModuleContractModel, ContractField
)
from repopackage.nldb_engine.engine import render_nl_doc, extract_nl_doc

def test_task_model_roundtrip():
    original = TaskModel(
        id="T-01",
        title="Test Task",
        traits=["Action", "Python"],
        explanation="Testing the new engine",
        what_to_fix="Fix the parser",
        how_to_do_it="Use AST",
        depends_on=["T-00"]
    )
    md = render_nl_doc(original)
    extracted = extract_nl_doc(TaskModel, md)
    assert extracted.id == original.id
    assert extracted.explanation == original.explanation
    # Traits use jinja2 (one-way), so we don't expect them back in 'data' 
    # unless we use rev| for them. Currently they are non-recoverable.

def test_pill_model_roundtrip():
    original = PillModel(
        title="Design Pattern",
        metadata=PillMetadata(id="PILL-01", type="pattern", scope="global", language="en", nature="context"),
        why="Clarity",
        what="Rules",
        how="Implement x"
    )
    md = render_nl_doc(original)
    extracted = extract_nl_doc(PillModel, md)
    assert extracted.metadata.id == original.metadata.id
    assert extracted.why == original.why
    assert extracted.metadata.type == "pattern"

def test_board_model_roundtrip():
    original = BoardModel(
        phases=[PhaseModel(id="1", tasks=["T-01", "T-02"])],
        pills=["PILL-01"]
    )
    md = render_nl_doc(original)
    extracted = extract_nl_doc(BoardModel, md)
    assert len(extracted.phases) == 1
    assert extracted.phases[0].tasks == ["T-01", "T-02"]

def test_module_contract_yaml_roundtrip():
    original = ModuleContractModel(
        module_name="nldb",
        version="1.0.0",
        description="The engine",
        inputs=[ContractField(name="raw", type="str", description="markdown")],
        traits=["Logic"]
    )
    md = render_nl_doc(original)
    # This renders as YAML. Let's see if the extractor handles it.
    extracted = extract_nl_doc(ModuleContractModel, md)
    assert extracted.module_name == "nldb"
    assert len(extracted.inputs) == 1
    assert extracted.inputs[0].name == "raw"
