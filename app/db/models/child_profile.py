from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from db.dependency import PyObjectId

class ChildProfile(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Optional[str] = None
    notes: Optional[str] = None

class ChildCreate(BaseModel):
    user_id: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: datetime
    gender: Optional[str] = None
    notes: Optional[str] = None