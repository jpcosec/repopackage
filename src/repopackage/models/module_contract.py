from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field
from repopackage.models.base import BaseArtifactModel


class ContractField(BaseModel):
    name: str
    type: str
    description: str


class ValidationState(BaseModel):
    unit_tests: bool = False
    contract_tests: bool = False
    linting_passed: bool = False


class ModuleContractModel(BaseArtifactModel):
    __template__: ClassVar[str] = "module_contract.yaml.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "yaml"

    module_name: str
    version: str
    description: str
    inputs: List[ContractField] = Field(default_factory=list)
    outputs: List[ContractField] = Field(default_factory=list)
    traits: List[str] = Field(default_factory=list)
    validation: ValidationState = Field(default_factory=ValidationState)
