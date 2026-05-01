import pytest
from unittest.mock import MagicMock
from repopackage.core.solver import CompositionSolver
from repopackage.core.models import IntegrationContract


def _solver(mock_git):
    return CompositionSolver(mock_git)


def test_resolve_empty_project(mock_git):
    lock = _solver(mock_git).resolve({"name": "root", "uses": {}})
    assert lock["project"] == "root"
    assert lock["repopackages"] == {}
    assert lock["compatibility"]["status"] == "passed"


def test_resolve_single_dep_appears_in_lockfile(mock_git):
    lock = _solver(mock_git).resolve({
        "name": "root",
        "uses": {"lib": {"url": "/tmp/lib", "branch": "main"}},
    })
    assert "lib" in lock["repopackages"]
    assert lock["repopackages"]["lib"]["branch"] == "main"
    assert lock["repopackages"]["lib"]["commit"] == "abc123"


def test_duplicate_dep_accumulates_constraints(mock_git):
    """Multiple parents declaring the same dep should accumulate all constraints."""
    s = _solver(mock_git)
    s.graph.add_node("root", type="project", contract=None, constraints=[])
    s._add_or_update_node("root", "lib", "/tmp/lib", "main", {"version": "^1.0.0"})
    s._add_or_update_node("root2", "lib", "/tmp/lib", "main", {"version": "^1.5.0"})
    assert "^1.0.0" in s.graph.nodes["lib"]["constraints"]
    assert "^1.5.0" in s.graph.nodes["lib"]["constraints"]


def test_cycle_detection_raises(mock_git):
    s = _solver(mock_git)
    s.graph.add_edge("a", "b")
    s.graph.add_edge("b", "a")
    with pytest.raises(Exception, match="FAILED_CYCLE"):
        s._check_cycles()


def test_no_cycle_passes(mock_git):
    s = _solver(mock_git)
    s.graph.add_edge("root", "a")
    s.graph.add_edge("a", "b")
    s._check_cycles()


def test_transitive_url_fabrication_raises(mock_git):
    """Bug #4 Fix: solver should NOT fabricate URLs. It should raise ValueError."""
    s = _solver(mock_git)
    # Pydantic will now coerce "^1.0.0" into a DependencySpec(version="^1.0.0", url=None)
    contract = IntegrationContract(
        name="lib", version="1.0.0",
        compatibility={"requires": {"sub-dep": {"version": "^1.0.0"}}},
    )
    with pytest.raises(ValueError, match="Missing URL for dependency 'sub-dep'"):
        s._expand_transitive("lib", contract)


def test_transitive_resolution_works_with_explicit_urls(mock_git):
    """Transitive deps work when the contract provides explicit URLs."""
    s = _solver(mock_git)
    contract = IntegrationContract(
        name="lib", version="1.0.0",
        compatibility={"requires": {
            "sub-dep": {"url": "git@github.com:org/sub.git", "version": "^1.0.0"}
        }},
    )
    s._expand_transitive("lib", contract)
    # Check that sub-dep was added to graph
    assert "sub-dep" in s.graph.nodes
    called_url = mock_git.get_commit_hash.call_args[0][0]
    assert called_url == "git@github.com:org/sub.git"


def test_bad_contract_yaml_is_not_swallowed(mock_git):
    """Bug #7 Fix: malformed contract raises RuntimeError."""
    mock_git.read_file.side_effect = ValueError("malformed yaml")
    s = _solver(mock_git)
    with pytest.raises(RuntimeError, match="Failed to load/parse contract"):
        s.resolve({"name": "root", "uses": {"lib": {"url": "/x", "branch": "m"}}})
