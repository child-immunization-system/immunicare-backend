from fastapi import APIRouter, Depends, HTTPException
from db.repositories.milestone import MilestoneRepository
from db.models.milestone import Milestone

router = APIRouter()

@router.post("/")
async def create_milestone(milestone: Milestone, repo: MilestoneRepository = Depends()):
    await repo.create_milestone(milestone)
    return {"msg": "Milestone created successfully"}

@router.get("/{child_id}")
async def get_milestones(child_id: str, repo: MilestoneRepository = Depends()):
    milestones = await repo.get_milestones_by_child_id(child_id)
    if not milestones:
        raise HTTPException(status_code=404, detail="No milestones found for the child")
    return milestones
