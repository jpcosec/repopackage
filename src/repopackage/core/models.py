"""
Unified domain models for Repopackage.
"""
from typing import List, Dict, Optional
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

class IntegrationContract(BaseModel):
    name: str
    version: str
    exports: List[Schema] = []
    consumes: List[Schema] = []
    # Keyed by category (e.g. 'requires'), value is a map of pkg_name -> DependencySpec
    compatibility: Dict[str, Dict[str, DependencySpec]] = {}

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

