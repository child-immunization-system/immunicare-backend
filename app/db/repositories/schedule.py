from db.models.schedule import Schedule

class ScheduleRepository:
    def __init__(self, database):
        self.database = database

    async def create_schedule(self, schedule: Schedule):
        await self.database["schedules"].insert_one(schedule.dict())

    async def get_schedules_by_child_id(self, child_id: str):
        return await self.database["schedules"].find({"child_id": child_id}).to_list(length=100)
