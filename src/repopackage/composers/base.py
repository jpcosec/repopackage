from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from repopackage.models.base import BaseArtifactModel
from repopackage.artifact.interface import ArtifactInterface

Out = TypeVar("Out", bound=BaseArtifactModel)


class Composer(ABC, Generic[Out]):
    @abstractmethod
    def compose(self) -> ArtifactInterface[Out]:
        ...
