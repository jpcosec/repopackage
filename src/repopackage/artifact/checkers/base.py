from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from repopackage.models.base import BaseArtifactModel
from repopackage.artifact.result import CheckResult

M = TypeVar("M", bound=BaseArtifactModel)


class ArtifactChecker(ABC, Generic[M]):
    @abstractmethod
    def check(self, model: M) -> CheckResult:
        ...
