from enum import Enum
from typing import ClassVar, List, Literal, Optional
from pydantic import Field
from repopackage.models.base import BaseArtifactModel


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TaskLifecycle(str, Enum):
    TARGET = "target"
    CURRENT = "current"


class TaskModel(BaseArtifactModel):
    __template__: ClassVar[str] = "task.md.jinja2"
    __format__: ClassVar[Literal["markdown", "yaml"]] = "markdown"

    id: str
    title: str
    traits: List[str] = Field(default_factory=list)
    explanation: str
    reference: List[str] = Field(default_factory=list)
    what_to_fix: str
    how_to_do_it: str
    induced_changes: Optional[str] = None
    depends_on: List[str] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.P2
    status: TaskStatus = TaskStatus.OPEN
    lifecycle: TaskLifecycle = TaskLifecycle.TARGET
    phase: Optional[str] = None
    pills: List[str] = Field(default_factory=list)
    commit_sha: Optional[str] = None
