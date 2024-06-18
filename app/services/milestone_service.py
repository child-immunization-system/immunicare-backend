from db.models.milestone import Milestone
from db.repositories.milestone import MilestoneRepository

class MilestoneService:
    def __init__(self, repository: MilestoneRepository):
        self.repository = repository

    async def create_milestone(self, milestone: Milestone):
        await self.repository.create_milestone(milestone)

    async def get_milestones_by_child_id(self, child_id: str):
        return await self.repository.get_milestones_by_child_id(child_id)
