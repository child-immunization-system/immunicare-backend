from pydantic import BaseModel
from datetime import date
from typing import Optional

class Immunization(BaseModel):
    id: str
    child_id: str
    vaccine_name: str
    date_administered: date
    next_due_date: date
    notes: Optional[str] = None
