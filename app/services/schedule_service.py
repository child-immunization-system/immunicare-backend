from datetime import datetime, timedelta

from pydantic import BaseModel
from db.models.schedule import CreateSchedule
from db.repositories.schedule import ScheduleRepository

immune_schedules = {
    "birth": ["BCG", "OPV-O"],
    "6_weeks": ["Penta-1", "OPV-1", "PCV-1", "Rota-1"],
    "10_weeks": ["Penta-2", "OPV-2", "PCV-2", "Rota-2"],
    "14_weeks": ["Penta-3", "OPV-3", "PCV-3", "IPV"],
    "9_months": ["Measles-1", "Yellow Fever"],
    "12_months": ["MenA"]
}
immune_schedule_days = {
    "birth": 0,
    "6_weeks": 6 * 7,
    "10_weeks": 10 * 7,
    "14_weeks": 14 * 7,
    "9_months": 9 * 30,
    "12_months": 12 * 30,
}

class vaccinationDates(BaseModel):
    period: str
    vaccination: list
    due_date: datetime

    
class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    async def create_schedule(self, schedule: CreateSchedule):
        await self.repository.create_schedule(schedule)

    async def get_schedules_by_child_id(self, child_id: str):
        return await self.repository.get_schedules_by_child_id(child_id)

    @classmethod
    async def create_child_schedule(self, date_of_birth: datetime | str ) -> list[vaccinationDates]:
        
        vaccinations_due = []
        
        for period, days in immune_schedule_days.items():
            schedule = vaccinationDates(
                period=period,
                vaccination=immune_schedules[period],
                due_date= (date_of_birth + timedelta(days=days)).strftime("%Y-%m-%d")
            )
            vaccinations_due.append(schedule)
        
        return vaccinations_due