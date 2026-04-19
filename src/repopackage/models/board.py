from typing import ClassVar, List, Dict
from pydantic import BaseModel, Field
from repopackage.models.base import BaseArtifactModel

class PhaseModel(BaseModel):
    id: str
    tasks: List[str] = Field(default_factory=list)

class BoardModel(BaseArtifactModel):
    __template__: ClassVar[str] = """
# Board

⸢rev,table•phases⸥

## Pills
⸢rev,table•pills⸥
""".strip()

    phases: List[PhaseModel] = Field(default_factory=list)
    pills: List[str] = Field(default_factory=list)
