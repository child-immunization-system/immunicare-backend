from pydantic import BaseModel
from datetime import date
from typing import Optional

class Milestone(BaseModel):
    id: str
    child_id: str
    milestone_name: str
    date_achieved: Optional[date] = None
    notes: Optional[str] = None
