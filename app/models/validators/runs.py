from enum import Enum
from datetime import datetime
from typing import Optional
from typing import List


from pydantic import BaseModel
from pydantic import Json


class RunStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    ENDED = "ENDED"


class RunsDB(BaseModel):
    id: str
    user_id: str
    status: RunStatus
    description: Optional[str]
    distance: Optional[float]
    speed: Optional[float]
    weather: Optional[str]
    created_at: datetime
    updated_at: datetime


class RunUpdate(BaseModel):
    id: str
    status: Optional[RunStatus]
    description: Optional[str]
    distance: Optional[float]
    speed: Optional[float]
    weather: Optional[str]


class RunsColumnSummary(BaseModel):
    mean: Optional[float]
    min: Optional[float]
    max: Optional[float]


class RunsSummary(BaseModel):
    distance: RunsColumnSummary
    speed: RunsColumnSummary


class RunsReport(BaseModel):
    runs: List[RunsDB]
    summary: Optional[RunsSummary]
