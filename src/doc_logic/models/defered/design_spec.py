from typing import ClassVar, Literal
from repopackage.models.base import BaseArtifactModel


class DesignSpecModel(BaseArtifactModel):
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    name: str
    layer_0: str
    layer_1: str
    layer_2: str
    layer_3: str
    layer_4: str
    layer_5: str
