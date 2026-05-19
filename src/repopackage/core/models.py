"""
Unified domain models for Repopackage.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, model_validator


class Schema(BaseModel):
    """A formal schema definition or reference."""
    name: str = Field(description="Unique identifier for this schema.")
    path: str = Field(..., alias="schema", description="Filesystem path to the schema definition.")


class Traits(BaseModel):
    """Project-specific traits and tool preferences."""
    formatter: Optional[str] = Field(None, description="Preferred code formatter.")
    test_runner: Optional[str] = Field(None, description="Preferred test runner command.")
    lang: str = Field("python", alias="preferred_language", description="Primary programming language.")


class DependencySpec(BaseModel):
    """Explicit intent for a dependency resolution."""
    url: Optional[str] = Field(None, description="Git remote URL or local path.")
    branch: Optional[str] = Field("master", description="Git branch to track.")
    version: str = Field("*", description="Semantic version constraint (e.g., '^1.0.0').")
    commit: Optional[str] = Field(None, description="Specific git commit hash (pinning).")
    line: Optional[str] = Field(None, description="Ecosystem 'line' identifier (e.g. 'central').")


class CommandExport(BaseModel):
    """An executable command exposed by a package."""
    name: str = Field(description="The command name as invoked through rp.")
    description: str = Field(description="Human-readable summary of what the command does.")
    entrypoint: str = Field(description="The python module/function or shell path to execute.")
    args: Dict[str, str] = Field(default_factory=dict, description="Expected arguments and their descriptions.")
    env: Dict[str, str] = Field(default_factory=dict, description="Required environment variables.")


class ContractExport(BaseModel):
    """A formal contract schema exposed by a package."""
    name: str = Field(description="The contract identifier.")
    description: str = Field(description="What this contract governs.")
    schema_ref: str = Field(description="A reference to the Pydantic model or JSON schema.")
    version: str = Field(description="The semantic version of the contract.")


class ProcedureExport(BaseModel):
    """A multi-step deterministic procedure."""
    name: str = Field(description="The procedure name.")
    description: str = Field(description="The intent of the procedure.")
    steps: List[str] = Field(description="Ordered list of step identifiers or descriptions.")
    inputs: List[str] = Field(default_factory=list, description="Required input identifiers.")
    outputs: List[str] = Field(default_factory=list, description="Produced output identifiers.")


class SurfaceExport(BaseModel):
    """A materializable UI or documentation surface."""
    name: str = Field(description="The surface name.")
    description: str = Field(description="What this surface visualizes.")
    mount_path: str = Field(description="Where this surface is mounted in the virtual tree.")
    provider: str = Field(description="The technology provider (e.g., 'react', 'markdown').")


class ExportSurface(BaseModel):
    """The canonical export model that packages use to expose capabilities."""
    package_name: str = Field(description="The name of the exporting package.")
    version: str = Field(description="The version of the export surface.")
    commands: Dict[str, CommandExport] = Field(default_factory=dict, description="Exposed CLI commands.")
    aliases: Dict[str, str] = Field(default_factory=dict, description="Map of alias -> command_name.")
    contracts: Dict[str, ContractExport] = Field(default_factory=dict, description="Exposed formal contracts.")
    procedures: Dict[str, ProcedureExport] = Field(default_factory=dict, description="Exposed procedures.")
    surfaces: Dict[str, SurfaceExport] = Field(default_factory=dict, description="Exposed UI/Doc surfaces.")
    precedence: int = Field(default=100, description="Merge precedence: lower values win.")
    provenance: Dict[str, Any] = Field(default_factory=dict, description="Audit metadata (source repo, commit).")


class IntegrationContract(BaseModel):
    """The formal contract between a package and the ecosystem."""
    name: str = Field(description="The canonical package name.")
    version: str = Field(description="The package semantic version.")
    exports: List[Schema] = Field(default_factory=list, description="List of schemas exported by this package.")
    consumes: List[Schema] = Field(default_factory=list, description="List of schemas consumed by this package.")
    compatibility: Dict[str, Dict[str, DependencySpec]] = Field(
        default_factory=dict,
        description="Dependency constraints keyed by category (e.g. 'requires')."
    )
    export_surface: Optional[ExportSurface] = Field(None, description="The full capability export surface.")


class ComposableUnit(BaseModel):
    """Base unit of composition in the ecosystem."""
    name: str = Field(description="The name of the unit.")
    url: str = Field(description="The source URL or path.")
    branch: str = Field("master", description="The tracked branch.")
    commit: Optional[str] = Field(None, description="The specific resolved commit.")
    contract: Optional[IntegrationContract] = Field(None, description="The resolved integration contract.")
    traits: Optional[Traits] = Field(None, description="Tooling and language traits.")


class Project(ComposableUnit):
    """The root unit of a composition."""
    uses: Dict[str, DependencySpec] = Field(default_factory=dict, description="Direct dependencies of the project.")


class ResolvedPackage(BaseModel):
    """Actual materialized state of a package in the workspace."""
    name: str = Field(description="The package name.")
    url: str = Field(description="The source URL.")
    branch: str = Field(description="The branch used for resolution.")
    commit: str = Field(description="The resolved commit SHA.")
    line: Optional[str] = Field(None, description="The ecosystem line used.")
    compatibility_status: str = Field("passed", description="Result of the solver validation.")
    exports: Optional[ExportSurface] = Field(None, description="The resolved export surface.")


class Lockfile(BaseModel):
    """The schema for compose.lock.yaml."""
    version: str = Field("1.0", description="Schema version of the lockfile.")
    project: str = Field(..., description="Name of the root project.")
    packages: Dict[str, ResolvedPackage] = Field(default_factory=dict, description="Map of resolved packages.")
    repopackages: Dict[str, ResolvedPackage] = Field(default_factory=dict, description="Legacy alias for packages.")
    manifest_hash: str = Field(..., description="Hash of the input composition and graph state.")
    resolved_at: str = Field(..., description="ISO timestamp of the resolution event.")

    @model_validator(mode='after')
    def sync_packages(self) -> 'Lockfile':
        """Ensures 'packages' and 'repopackages' are kept in sync for legacy compatibility."""
        if self.packages and not self.repopackages:
            self.repopackages = self.packages
        elif self.repopackages and not self.packages:
            self.packages = self.repopackages
        return self
