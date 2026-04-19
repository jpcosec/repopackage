from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar
from repopackage.models.base import BaseArtifactModel

M = TypeVar("M", bound=BaseArtifactModel)


class ArtifactParser(ABC, Generic[M]):
    def __init__(self, model_class: Type[M]):
        self.model_class = model_class

    @abstractmethod
    def parse(self, raw: str) -> M:
        ...
