import yaml
from typing import TypeVar
from repopackage.artifact.parsers.base import ArtifactParser
from repopackage.models.base import BaseArtifactModel

M = TypeVar("M", bound=BaseArtifactModel)


class YamlParser(ArtifactParser[M]):
    def parse(self, raw: str) -> M:
        data = yaml.safe_load(raw)
        return self.model_class.model_validate(data)
