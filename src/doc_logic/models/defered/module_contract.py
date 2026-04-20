from typing import Any, ClassVar, Dict, List, Literal
from pydantic import BaseModel, Field, model_validator
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
    __format__: ClassVar[Literal["markdown", "yaml"]] = "yaml"

    @model_validator(mode="before")
    @classmethod
    def _flatten_interface(cls, data: Any) -> Any:
        if isinstance(data, dict) and "interface" in data:
            iface = data.pop("interface") or {}
            data.setdefault("inputs", iface.get("inputs", []))
            data.setdefault("outputs", iface.get("outputs", []))
        return data

    module_name: str
    version: str
    description: str
    inputs: List[ContractField] = Field(default_factory=list)
    outputs: List[ContractField] = Field(default_factory=list)
    traits: List[str] = Field(default_factory=list)
    validation: ValidationState = Field(default_factory=ValidationState)
