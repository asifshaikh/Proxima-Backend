from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class HackathonCreateSchema(BaseModel):
    event_name: str = Field(..., min_length=3)
    organizer_id: str

    description: Optional[str]
    location: Optional[str]

    mode: str = Field(..., pattern="^(online|offline|hybrid)$")
    participation_type: str = Field(..., pattern="^(individual|team)$")

    min_team_size: Optional[int]
    max_team_size: Optional[int]

    deadline: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    entry_fee: float = 0
    max_participants: Optional[int]

    tags: Optional[List[str]] = []

class HackathonResponse(BaseModel):
    id: str
    event_name: str
    organizer_id: str
    description: Optional[str]
    location: Optional[str]
    mode: str
    participation_type: str
    min_team_size: Optional[int]
    max_team_size: Optional[int]
    deadline: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    entry_fee: float
    max_participants: Optional[int]
    tags: List[str]
    created_at: datetime

    class Config:
        from_attributes = True  


class HackathonUpdateSchema(BaseModel):
    event_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    mode: Optional[str] = None
    participation_type: Optional[str] = None

    min_team_size: Optional[int] = None
    max_team_size: Optional[int] = None

    deadline: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    entry_fee: Optional[float] = None
    max_participants: Optional[int] = None
    tags: Optional[List[str]] = None

    model_config = {
        "extra": "forbid"
    }