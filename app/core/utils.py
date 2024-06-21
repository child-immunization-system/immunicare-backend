from datetime import datetime
from db.models.schedule import CreateSchedule
from db.models.child_profile import ChildProfile
from db.dependency import get_database
from db.repositories.schedule import ScheduleRepository
from services.schedule_service import ScheduleService


# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from core.config import settings

# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,
#     MAIL_PASSWORD=settings.MAIL_PASSWORD,
#     MAIL_FROM=settings.MAIL_FROM,
#     MAIL_PORT=settings.MAIL_PORT,
#     MAIL_SERVER=settings.MAIL_SERVER,
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )

# async def send_reset_password_email(email: str, token: str):
#     reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
#     message = MessageSchema(
#         subject="Password Reset Request",
#         recipients=[email],
#         body=f"Please use the following link to reset your password: {reset_url}",
#         subtype="html"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)



schedule_repo = ScheduleRepository(get_database)
schedule_servcice = ScheduleService(schedule_repo)


async def create_child_plan(mother_id, child, db):
    schedules_repo = ScheduleRepository(db)
    child = ChildProfile(**child)

    if type(child.date_of_birth) is not datetime:
            child.date_of_birth = datetime.strptime(child.date_of_birth, "%Y-%m-%d")

    schedules = await schedule_servcice.create_child_schedule(child.date_of_birth)

    for schedule in schedules:
        new_schedule = CreateSchedule(
            child_id=child.id,
            event_name=f"Vaccination of {child.first_name} {child.first_name} at {schedule.period}",
            event_date=child.date_of_birth,
            vaccination=schedule.vaccination,
        )

        await schedules_repo.create_schedule(new_schedule)
