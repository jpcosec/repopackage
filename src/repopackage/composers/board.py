from typing import List
from repopackage.artifact.interface import ArtifactInterface
from repopackage.composers.base import Composer
from repopackage.models.board import BoardModel, PhaseModel
from repopackage.models.task import TaskModel


class BoardComposer(Composer[BoardModel]):
    def __init__(self, tasks: List[ArtifactInterface[TaskModel]]):
        self._tasks = tasks

    def compose(self) -> ArtifactInterface[BoardModel]:
        phase_map: dict[str, list[str]] = {}
        for artifact in self._tasks:
            phase_id = artifact.model.phase or "1"
            phase_map.setdefault(phase_id, []).append(artifact.model.id)
        phases = [PhaseModel(id=pid, tasks=tids) for pid, tids in sorted(phase_map.items())]
        return ArtifactInterface(model=BoardModel(phases=phases, pills=[]))
