from typing import List, Optional
from pydantic import BaseModel, Field

class PillMetadata(BaseModel):
    id: str = Field(..., alias="ID")
    type: str = Field(..., alias="Type")
    scope: str = Field(..., alias="Scope")
    language: str = Field(..., alias="Language")
    nature: str = Field(..., alias="Nature")

class PillModel(BaseModel):
    title: str
    metadata: PillMetadata
    why: str
    what: str
    how: str
    lifecycle: str = "Still needed? (Keep)"
