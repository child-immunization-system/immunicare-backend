from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Schedule(BaseModel):
    id: str
    child_id: str
    event_name: str
    event_date: datetime
    notes: Optional[str] = None
