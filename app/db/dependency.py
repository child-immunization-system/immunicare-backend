from typing import Annotated
from pydantic import BeforeValidator
from db.base import database

def get_database():
    return database

PyObjectId = Annotated[str, BeforeValidator(str)]