from typing import List, ClassVar
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
    __template__: ClassVar[str] = """
module_name: "⸢rev•module_name⸥"
version: "⸢rev•version⸥"
description: "⸢rev•description⸥"
interface:
  inputs:
⸢rev,table•inputs⸥
  outputs:
⸢rev,table•outputs⸥
traits:
⸢jinja2•{% for t in traits %}  - "{{ t }}"
{% endfor %}⸥
validation:
  unit_tests: ⸢jinja2•{{ validation.unit_tests | lower }}⸥
  contract_tests: ⸢jinja2•{{ validation.contract_tests | lower }}⸥
  linting_passed: ⸢jinja2•{{ validation.linting_passed | lower }}⸥
""".strip()

    module_name: str
    version: str
    description: str
    inputs: List[ContractField] = Field(default_factory=list)
    outputs: List[ContractField] = Field(default_factory=list)
    traits: List[str] = Field(default_factory=list)
    validation: ValidationState = Field(default_factory=ValidationState)
