from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from db.models.child_profile import ChildProfile
from db.dependency import get_database
from db.repositories.child_profile import ChildProfileRepository
from db.repositories.schedule import ScheduleRepository
from db.models.schedule import Schedule

router = APIRouter()

immune_schedules = {
    "birth": ["BCG", "OPV-O"],
    "6_weeks": ["Penta-1", "OPV-1", "PCV-1", "Rota-1"],
    "10_weeks": ["Penta-2", "OPV-2", "PCV-2", "Rota-2"],
    "14_weeks": ["Penta-3", "OPV-3", "PCV-3", "IPV"],
    "9_months": ["Measles-1", "Yellow Fever"],
    "12_months": ["MenA"]
}
immune_schedule_days = {
    "birth": 0,
    "6_weeks": 6 * 7,
    "10_weeks": 10 * 7,
    "14_weeks": 14 * 7,
    "9_months": 9 * 30,
    "12_months": 12 * 30,
}

class vaccinationDates(BaseModel):
    period: str
    vaccination: list
    due_date: datetime


@router.post("/")
async def create_schedule(schedule: Schedule, db=Depends(get_database)):
    repo = ScheduleRepository(db)
    await repo.create_schedule(schedule)
    return {"msg": "Schedule created successfully"}


@router.get("/vaccine-schedule")
async def get_schedules(child_id=Query(str), db=Depends(get_database)):
    child_repo = ChildProfileRepository(db)
    """schedules = await repo.get_schedules_by_child_id(child_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found for the child")
    return schedules"""

    child = await child_repo.get_child_profile_by_id(child_id)
    if not child:
        raise HTTPException(status_code=404, detail="No child with the provided id found")
    child = ChildProfile(**child)

    try:
        if type(child.date_of_birth) is not datetime:
            birth_date_parsed = datetime.strptime(child.date_of_birth, "%Y-%m-%d")
        birth_date_parsed = child.date_of_birth
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, should be YYYY-MM-DD")

    vaccinations_due = []
    for period, days in immune_schedule_days.items():
        schedule = vaccinationDates(
            period=period,
            vaccination=immune_schedules[period],
            due_date= (birth_date_parsed + timedelta(days=days)).strftime("%Y-%m-%d")
        )
        vaccinations_due.append(schedule)

    return vaccinations_due