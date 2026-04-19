from enum import Enum
from typing import List, Optional, ClassVar
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
    __template__: ClassVar[str] = """
# ⸢rev|id⸥ - ⸢rev|title⸥

## Traits (Composición)
`⸢jinja2|{{ traits | join(' | ') }}⸥`

## Explanation
⸢rev|explanation⸥

## Reference
⸢jinja2|{% for ref in reference %}- `{{ ref }}`
{% endfor %}⸥

## What to Fix / Implement
⸢rev|what_to_fix⸥

## How to Do It (Suggested)
⸢rev|how_to_do_it⸥

## Induced Changes
⸢revop|induced_changes⸥

## Depends On
⸢jinja2|{% for dep in depends_on %}- {{ dep }}
{% endfor %}⸥

## Priority
⸢rev|priority⸥

---
**Status:** ⸢rev|status⸥
**Lifecycle:** ⸢rev|lifecycle⸥
**Commit SHA:** ⸢revop|commit_sha⸥
""".strip()

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
    commit_sha: Optional[str] = None
    
    # Hidden fields for internal logic
    phase: Optional[str] = None
    pills: List[str] = Field(default_factory=list)
