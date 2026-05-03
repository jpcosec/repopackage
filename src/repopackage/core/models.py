"""
Unified domain models for Repopackage.
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, model_validator

class Schema(BaseModel):
    name: str
    path: str = Field(..., alias="schema")

class Traits(BaseModel):
    formatter: Optional[str] = None
    test_runner: Optional[str] = None
    lang: str = Field("python", alias="preferred_language")

class DependencySpec(BaseModel):
    """Explicit intent for a dependency."""
    url: Optional[str] = None
    branch: Optional[str] = "master"
    version: str = "*"
    commit: Optional[str] = None
    line: Optional[str] = None

# --- Export Surface Models (Task 010) ---

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
    commands: Dict[str, CommandExport] = Field(default_factory=dict)
    aliases: Dict[str, str] = Field(default_factory=dict, description="Map of alias -> command_name.")
    contracts: Dict[str, ContractExport] = Field(default_factory=dict)
    procedures: Dict[str, ProcedureExport] = Field(default_factory=dict)
    surfaces: Dict[str, SurfaceExport] = Field(default_factory=dict)
    
    # Precedence and Provenance
    precedence: int = Field(default=100, description="Merge precedence: lower values win.")
    provenance: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Audit metadata (source repo, commit, resolved_at)."
    )

# --- Integration and Composition ---

class IntegrationContract(BaseModel):
    name: str
    version: str
    exports: List[Schema] = []
    consumes: List[Schema] = []
    # Keyed by category (e.g. 'requires'), value is a map of pkg_name -> DependencySpec
    compatibility: Dict[str, Dict[str, DependencySpec]] = {}
    
    # New: Full export surface support
    export_surface: Optional[ExportSurface] = None

class ComposableUnit(BaseModel):
    name: str
    url: str
    branch: str = "master"
    commit: Optional[str] = None
    contract: Optional[IntegrationContract] = None
    traits: Optional[Traits] = None

class Project(ComposableUnit):
    uses: Dict[str, DependencySpec] = {}

class ResolvedPackage(BaseModel):
    """Actual materialized state of a package in the workspace."""
    name: str
    url: str
    branch: str
    commit: str
    line: Optional[str] = None
    compatibility_status: str = "passed"
    # New: resolved export surface
    exports: Optional[ExportSurface] = None

class Lockfile(BaseModel):
    """The compose.lock.yaml schema."""
    version: str = "1.0"
    project: str = Field(..., description="Project name")
    packages: Dict[str, ResolvedPackage] = {}
    repopackages: Dict[str, ResolvedPackage] = {}
    manifest_hash: str = Field(..., description="Hash of the compose.yaml at resolution time")
    resolved_at: str = Field(..., description="ISO timestamp of resolution")

    @model_validator(mode='after')
    def sync_packages(self) -> 'Lockfile':
        if self.packages and not self.repopackages:
            self.repopackages = self.packages
        elif self.repopackages and not self.packages:
            self.packages = self.repopackages
        return self
