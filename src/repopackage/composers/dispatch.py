from typing import List
from repopackage.artifact.interface import ArtifactInterface
from repopackage.models.task import TaskModel
from repopackage.models.pill import PillModel


class DispatchPackageComposer:
    def __init__(self, task: ArtifactInterface[TaskModel], pills: List[ArtifactInterface[PillModel]]):
        self._task = task
        self._pills = pills

    def compose(self) -> str:
        parts = [self._task.to_agent()]
        for pill in self._pills:
            parts.append(pill.to_agent())
        return "---\n".join(parts)
