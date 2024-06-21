from bson import ObjectId
from db.models.child_profile import ChildCreate, ChildProfile
from motor.motor_asyncio import AsyncIOMotorDatabase

class ChildProfileRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database

    async def create_child_profile(self, profile: ChildProfile):
        await self.database["child_profiles"].insert_one(profile.dict())

    async def get_child_profile_by_id(self, profile_id: str):
        profile_id = profile_id if not isinstance(profile_id, str) else ObjectId(profile_id)
        return await self.database["child_profiles"].find_one({"_id": profile_id})
    
    async def get_child_profile_by_info(self, profile: ChildCreate):
        
        return await self.database["child_profiles"].find_one({"user_id": profile.user_id,
                                                               "first_name": profile.first_name,
                                                                "last_name": profile.last_name,
                                                                "date_of_birth": profile.date_of_birth,
                                                                "gender": profile.gender,
                                                                "notes": profile.notes
                                                               })

    async def get_child_profiles_by_user_id(self, user_id: str):
        return await self.database["child_profiles"].find({"user_id": user_id}).to_list(length=100)
