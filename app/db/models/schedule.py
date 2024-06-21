from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from db.dependency import PyObjectId

class Status(Enum):
    pending= "pending"
    complete = "complete"
    missed = "missed"


class Schedule(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    child_id: str
    event_name: str
    event_date: datetime
    vaccination: Optional[list] = None
    notified: Optional[bool] = False
    status: Optional[str] = "pending"
    notes: Optional[str] = None

class CreateSchedule(BaseModel):
    child_id: str
    event_name: str
    event_date: datetime
    vaccination: Optional[list] = None
    notified: Optional[bool] = False
    status: Optional[str] = "pending"
    notes: Optional[str] = None