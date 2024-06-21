from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from services.schedule_service import ScheduleService
from db.models.child_profile import ChildProfile
from db.dependency import get_database
from db.repositories.child_profile import ChildProfileRepository
from db.repositories.schedule import ScheduleRepository
from db.models.schedule import CreateSchedule

router = APIRouter()


schedule_servcice = ScheduleService(ScheduleRepository(get_database))


@router.post("/")
async def create_schedule(schedule: CreateSchedule, db=Depends(get_database)):
    repo = ScheduleRepository(db)
    await repo.create_schedule(schedule)
    return {"msg": "Schedule created successfully"}
#TODO: create a background function to create all milestones for a child after the schedule is created

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

    vaccinations_due = await schedule_servcice.create_child_schedule(birth_date_parsed)

    return vaccinations_due