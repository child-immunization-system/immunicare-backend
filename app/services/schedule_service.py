from db.models.schedule import Schedule
from db.repositories.schedule import ScheduleRepository

class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    async def create_schedule(self, schedule: Schedule):
        await self.repository.create_schedule(schedule)

    async def get_schedules_by_child_id(self, child_id: str):
        return await self.repository.get_schedules_by_child_id(child_id)
