from bson import ObjectId
from db.models.schedule import Schedule
from motor.motor_asyncio import AsyncIOMotorDatabase


class ScheduleRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database

    async def create_schedule(self, schedule: Schedule):
        await self.database["schedules"].insert_one(schedule.dict())

    async def get_schedules_by_child_id(self, child_id: str):
        return await self.database["schedules"].find({"child_id": child_id}).to_list(length=100)
    
    async def get_all_schedules(self):
        return await self.database["schedules"].find().to_list(None)

    async def update_schedule(self, schedule: Schedule):
        schedule_id = schedule.id if not isinstance(schedule.id, str) else ObjectId(schedule.id)
        schedule_dict = schedule.dict()
        await self.database["schedules"].update_many({"_id": schedule_id}, {"$set": schedule_dict})