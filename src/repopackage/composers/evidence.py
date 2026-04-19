import re
from repopackage.artifact.interface import ArtifactInterface
from repopackage.composers.base import Composer
from repopackage.models.evidence import EvidenceModel
from repopackage.models.task import TaskModel


class EvidenceComposer(Composer[EvidenceModel]):
    def __init__(self, task: ArtifactInterface[TaskModel], test_log: str, lint_log: str):
        self._task = task
        self._test_log = test_log
        self._lint_log = lint_log

    def compose(self) -> ArtifactInterface[EvidenceModel]:
        tests_ok = "failed" not in self._test_log
        lint_ok = not bool(re.search(r"(failed|error|[EWF]\d{3})", self._lint_log, re.IGNORECASE))
        model = EvidenceModel(
            task_id=self._task.model.id,
            passed=tests_ok and lint_ok,
            lint_ok=lint_ok,
            tests_ok=tests_ok,
            raw_log=self._test_log + "\n" + self._lint_log,
        )
        return ArtifactInterface(model=model)
