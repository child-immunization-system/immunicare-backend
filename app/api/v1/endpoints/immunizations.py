from fastapi import APIRouter, Depends, HTTPException
from db.repositories.immunization import ImmunizationRepository
from db.models.immunization import Immunization

router = APIRouter()

@router.post("/")
async def create_immunization(immunization: Immunization, repo: ImmunizationRepository = Depends()):
    await repo.create_immunization(immunization)
    return {"msg": "Immunization record created successfully"}

@router.get("/{child_id}")
async def get_immunizations(child_id: str, repo: ImmunizationRepository = Depends()):
    immunizations = await repo.get_immunizations_by_child_id(child_id)
    if not immunizations:
        raise HTTPException(status_code=404, detail="No immunizations found for the child")
    return immunizations
