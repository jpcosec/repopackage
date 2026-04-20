from typing import ClassVar, List, Literal
from pydantic import BaseModel, Field
from repopackage.models.base import BaseArtifactModel


class PhaseModel(BaseModel):
    id: str
    tasks: List[str] = Field(default_factory=list)


class BoardModel(BaseArtifactModel):
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    phases: List[PhaseModel] = Field(default_factory=list)
    pills: List[str] = Field(default_factory=list)
