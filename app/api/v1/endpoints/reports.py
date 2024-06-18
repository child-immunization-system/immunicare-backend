from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_report():
    return {"msg": "This is a placeholder for the reports endpoint"}
