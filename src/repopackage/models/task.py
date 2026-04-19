from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"

class TaskPriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"

class TaskModel(BaseModel):
    id: str = Field(..., description="Task ID (e.g., T-01)")
    title: str = Field(..., description="Task Title")
    traits: List[str] = Field(default_factory=list)
    explanation: str
    reference: List[str] = Field(default_factory=list)
    what_to_fix: str = Field(..., alias="what_to_fix_implement")
    how_to_do_it: str = Field(..., alias="how_to_do_it_suggested")
    induced_changes: Optional[str] = None
    depends_on: List[str] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.P2
    status: TaskStatus = TaskStatus.OPEN
    lifecycle: str = "target"
    commit_sha: Optional[str] = None
    phase: Optional[str] = None
    pills: List[str] = Field(default_factory=list)
