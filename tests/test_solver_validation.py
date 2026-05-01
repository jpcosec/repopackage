import pytest
from unittest.mock import MagicMock
from repopackage.core.solver import CompositionSolver
from repopackage.core.models import IntegrationContract, Schema


def _solver():
    m = MagicMock(
        get_commit_hash=MagicMock(return_value="x"),
        read_file=MagicMock(side_effect=FileNotFoundError),
    )
    return CompositionSolver(m)


def _add_pkg(s, name, version="1.0.0", constraints=None, exports=None, consumes=None):
    contract = IntegrationContract(
        name=name, version=version,
        exports=exports or [], consumes=consumes or [],
    )
    s.graph.add_node(name, type="pkg", url="x", branch="m", commit="a",
                     constraints=constraints or ["*"], contract=contract)
    return contract


def test_wildcard_constraint_always_passes():
    s = _solver()
    _add_pkg(s, "lib", "1.0.0", ["*"])
    s._check_version("lib", s.graph.nodes["lib"])


def test_satisfied_semver_constraint_passes():
    s = _solver()
    _add_pkg(s, "lib", "1.5.0", ["^1.0.0"])
    s._check_version("lib", s.graph.nodes["lib"])


def test_violated_semver_constraint_raises():
    s = _solver()
    _add_pkg(s, "lib", "1.0.0", ["^2.0.0"])
    with pytest.raises(Exception, match="VERSION_MISMATCH"):
        s._check_version("lib", s.graph.nodes["lib"])


def test_multiple_constraints_all_must_pass():
    s = _solver()
    _add_pkg(s, "lib", "1.5.0", ["^1.0.0", "^2.0.0"])
    with pytest.raises(Exception, match="VERSION_MISMATCH"):
        s._check_version("lib", s.graph.nodes["lib"])


def test_no_consumes_passes_interface_check():
    s = _solver()
    _add_pkg(s, "lib")
    s.graph.add_node("root", type="project", contract=None, constraints=[])
    s.graph.add_edge("root", "lib")
    s._check_interfaces("lib", s.graph.nodes["lib"])


def test_consumed_schema_satisfied_by_dependency():
    s = _solver()
    schema = Schema(name="MySchema", schema="schemas/s.json")
    _add_pkg(s, "consumer", consumes=[schema])
    _add_pkg(s, "provider", exports=[schema])
    s.graph.add_node("root", type="project", contract=None, constraints=[])
    s.graph.add_edge("root", "consumer")
    s.graph.add_edge("consumer", "provider")
    s._check_interfaces("consumer", s.graph.nodes["consumer"])


def test_unsatisfied_consumed_schema_raises():
    s = _solver()
    schema = Schema(name="Missing", schema="schemas/m.json")
    _add_pkg(s, "consumer", consumes=[schema])
    s.graph.add_node("root", type="project", contract=None, constraints=[])
    s.graph.add_edge("root", "consumer")
    with pytest.raises(Exception, match="CONTRACT_MISMATCH"):
        s._check_interfaces("consumer", s.graph.nodes["consumer"])
