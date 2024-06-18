from db.models.milestone import Milestone

class MilestoneRepository:
    def __init__(self, database):
        self.database = database

    async def create_milestone(self, milestone: Milestone):
        await self.database["milestones"].insert_one(milestone.dict())

    async def get_milestones_by_child_id(self, child_id: str):
        return await self.database["milestones"].find({"child_id": child_id}).to_list(length=100)
