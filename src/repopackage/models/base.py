from typing import ClassVar, Literal
from pydantic import BaseModel


class BaseArtifactModel(BaseModel):
    __template__: ClassVar[str] = ""
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"
