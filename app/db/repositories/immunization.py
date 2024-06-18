from db.models.immunization import Immunization

class ImmunizationRepository:
    def __init__(self, database):
        self.database = database

    async def create_immunization(self, immunization: Immunization):
        await self.database["immunizations"].insert_one(immunization.dict())

    async def get_immunizations_by_child_id(self, child_id: str):
        return await self.database["immunizations"].find({"child_id": child_id}).to_list(length=100)
