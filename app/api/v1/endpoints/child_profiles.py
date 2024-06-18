from fastapi import APIRouter, Depends, HTTPException, Path
from api.v1.endpoints.auth import get_current_user
from db.repositories.user import UserRepository
from db.models.user import User
from db.dependency import get_database
from db.repositories.child_profile import ChildProfileRepository
from db.models.child_profile import ChildCreate, ChildProfile

router = APIRouter()

@router.post("/")
async def create_child_profile(profile: ChildCreate , current_user=Depends(get_current_user), db=Depends(get_database)):
    mother_id = profile.user_id if profile.user_id else current_user["_id"]
    current_user = User(**current_user)
    profile.user_id = profile.user_id if profile.user_id else current_user.id

    repo = ChildProfileRepository(db)
    await repo.create_child_profile(profile)
    children = await repo.get_child_profiles_by_user_id(profile.user_id)
    
    children = [ChildProfile(**child) for child in children]
    children_id = [child.id for child in children if child.id not in current_user.children]
    
    current_user.children.extend(children_id)
    await add_child_to_mother(mother_id, current_user.children, db)
    return {"msg": "Child profile created successfully"}

@router.get("/{user_id}")
async def get_child_profiles(user_id= Path(), db=Depends(get_database)):
    repo = ChildProfileRepository(db)
    profiles = await repo.get_child_profiles_by_user_id(user_id)
    profiles = [ChildProfile(**profile) for profile in profiles]
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found for the user")
    return profiles

async def add_child_to_mother(mother_id, child_list: list, db):
    user_repo = UserRepository(db)
    await user_repo.update_user_children(mother_id, child_list)