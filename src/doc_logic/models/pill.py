from enum import Enum
from typing import ClassVar, Literal
from pydantic import BaseModel
from repopackage.models.base import BaseArtifactModel


class PillLifecycle(str, Enum):
    KEEP = "Keep"
    DELETE = "Delete"
    PROMOTE = "Promote"


class PillMetadata(BaseModel):
    id: str
    type: str
    scope: str
    language: str
    nature: str


class PillModel(BaseArtifactModel):
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    title: str
    metadata: PillMetadata
    why: str
    what: str
    when: str = ""
    where: str = ""
    how: str
    lifecycle: PillLifecycle = PillLifecycle.KEEP
