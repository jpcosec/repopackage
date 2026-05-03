from repopackage.core.models import ExportSurface, CommandExport, ContractExport

def test_export_surface_serialization():
    cmd = CommandExport(
        name="test-cmd",
        description="A test command",
        entrypoint="pkg.module:main",
        args={"arg1": "first argument"},
        env={"DEBUG": "1"}
    )
    
    contract = ContractExport(
        name="test-contract",
        description="A test contract",
        schema_ref="pkg.models:TestModel",
        version="1.0.0"
    )
    
    surface = ExportSurface(
        package_name="test-pkg",
        version="0.1.0",
        commands={"test-cmd": cmd},
        aliases={"tc": "test-cmd"},
        contracts={"test-contract": contract},
        precedence=10,
        provenance={"repo": "git@github.com:test/pkg.git", "commit": "abc123"}
    )
    
    data = surface.model_dump()
    assert data["package_name"] == "test-pkg"
    assert data["commands"]["test-cmd"]["entrypoint"] == "pkg.module:main"
    assert data["aliases"]["tc"] == "test-cmd"
    assert data["contracts"]["test-contract"]["version"] == "1.0.0"
    assert data["precedence"] == 10
    assert data["provenance"]["commit"] == "abc123"

    # Round trip
    surface2 = ExportSurface.model_validate(data)
    assert surface2.package_name == "test-pkg"
    assert isinstance(surface2.commands["test-cmd"], CommandExport)
    assert surface2.commands["test-cmd"].args["arg1"] == "first argument"
