from pathlib import Path
from typing import Generic, Type, TypeVar
import yaml
from jinja2 import Environment, PackageLoader

from repopackage.models.base import BaseArtifactModel
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel
from repopackage.models.module_contract import ModuleContractModel
from repopackage.artifact.result import CheckResult
from repopackage.artifact.parsers.markdown import MarkdownParser
from repopackage.artifact.parsers.yaml_parser import YamlParser
from repopackage.artifact.checkers.task import TaskChecker
from repopackage.artifact.checkers.board import BoardChecker
from repopackage.artifact.checkers.design_spec import DesignSpecChecker

M = TypeVar("M", bound=BaseArtifactModel)

_CHECKERS = {
    "TaskModel": TaskChecker(),
    "BoardModel": BoardChecker(),
    "DesignSpecModel": DesignSpecChecker(),
}


def _jinja_env() -> Environment:
    return Environment(loader=PackageLoader("repopackage", "templates"))


class ArtifactInterface(Generic[M]):
    def __init__(self, model: M):
        self.model = model

    @classmethod
    def from_disk(cls, model_class: Type[M], path: Path) -> "ArtifactInterface[M]":
        raw = path.read_text()
        if model_class.__format__ == "yaml":
            parser: YamlParser[M] | MarkdownParser[M] = YamlParser(model_class)
        else:
            parser = MarkdownParser(model_class)
        return cls(model=parser.parse(raw))

    @classmethod
    def create(cls, model_class: Type[M], **kwargs) -> "ArtifactInterface[M]":
        return cls(model=model_class(**kwargs))

    def to_disk(self, path: Path) -> None:
        env = _jinja_env()
        template = env.get_template(self.model.__template__)
        model_name = type(self.model).__name__.replace("Model", "").lower()
        path.write_text(template.render(**{model_name: self.model}))

    def to_agent(self) -> str:
        return yaml.dump(self.model.model_dump(mode="json"), allow_unicode=True, sort_keys=False)

    def check(self) -> CheckResult:
        checker = _CHECKERS.get(type(self.model).__name__)
        if checker is None:
            return CheckResult(passed=True, violations=[])
        return checker.check(self.model)
