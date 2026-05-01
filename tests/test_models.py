import pytest
from repopackage.core.models import (
    Schema, IntegrationContract, ComposableUnit, Project, Traits,
)


def test_schema_path_alias():
    s = Schema(name="MySchema", schema="schemas/my.json")
    assert s.path == "schemas/my.json"


def test_schema_missing_path_raises():
    with pytest.raises(Exception):
        Schema(name="Foo")


def test_contract_empty_defaults():
    c = IntegrationContract(name="pkg", version="1.0.0")
    assert c.exports == []
    assert c.consumes == []
    assert c.compatibility == {}


def test_composable_unit_branch_default():
    u = ComposableUnit(name="lib", url="git@gh.com:org/lib.git")
    assert u.branch == "master"
    assert u.commit is None
    assert u.contract is None


def test_project_uses_untyped():
    # Bug #8: uses is Dict[str, Dict[str, str]] — no DependencySpec model.
    # The 'line' field from the README/Architecture docs has no model backing.
    p = Project(name="app", url="u", uses={"dep": {"url": "x", "line": "feature"}})
    assert p.uses["dep"].line == "feature"


def test_traits_unused():
    # Bug #9: Traits is defined but never enforced or consumed anywhere.
    u = ComposableUnit(name="x", url="u", traits=None)
    assert u.traits is None
    t = Traits()
    assert t.formatter is None
