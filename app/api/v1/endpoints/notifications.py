from datetime import datetime
from fastapi import APIRouter, Depends
from db.models.child_profile import ChildProfile
from db.models.user import User
from db.repositories.child_profile import ChildProfileRepository
from db.repositories.user import UserRepository
from db.models.schedule import Schedule, Status
from db.dependency import get_database
from db.repositories.schedule import ScheduleRepository
from services.notification_service import NotificationService
from pydantic import BaseModel, EmailStr
router = APIRouter()

class NotificationRequest(BaseModel):
    email: EmailStr
    subject: str
    body: str

@router.post("/")
async def send_notification(request: NotificationRequest, service: NotificationService = Depends()):
    await service.send_notification(request.email, request.subject, request.body)
    return {"msg": "Notification sent successfully"}


async def send_schedule_notification():
    db = get_database()
    schedule_repo = ScheduleRepository(db)
    child_repo = ChildProfileRepository(db)
    user_repo = UserRepository(db)

    schedules = await schedule_repo.get_all_schedules()
    service = NotificationService()
    today = datetime.today()

    for schedule in schedules:
        schedule = Schedule(**schedule)

        child = await child_repo.get_child_profile_by_id(schedule.child_id)
        child = ChildProfile(**child)
        mother = await user_repo.get_user_by_id(child.user_id)
        mother = User(**mother)

        if today.year == schedule.event_date.year and today.month == schedule.event_date.month and today.day == schedule.event_date.day and schedule.status == "pending" and schedule.notified == False:
            await service.send_notification(email=mother.email, subject=schedule.event_name, body=str(schedule.vaccination))
            
            schedule.notified = True
            #schedule.status = "complete"

            schedule_repo.update_schedule(schedule)
        
        if today.year >= schedule.event_date.year or today.month >= schedule.event_date.month or today.day > schedule.event_date.day and schedule.status == "pending" and schedule.notified == True:
            #TODO: send a missed schedule
            await service.send_notification(email=mother.email, subject=schedule.event_name, body=str(schedule.vaccination))

            schedule.status = "missed"
            schedule_repo.update_schedule(schedule)