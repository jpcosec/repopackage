from typing import List, Optional
from pydantic import BaseModel


class Violation(BaseModel):
    rule: str
    message: str
    field: Optional[str] = None


class CheckResult(BaseModel):
    passed: bool
    violations: List[Violation]
