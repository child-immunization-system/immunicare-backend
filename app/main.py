from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import auth, child_profiles, immunizations, notifications, schedules, milestones, reports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", include_in_schema=True)
def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(child_profiles.router, prefix="/api/v1/child_profiles", tags=["Child Profiles"])
app.include_router(immunizations.router, prefix="/api/v1/immunizations", tags=["Immunizations"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(schedules.router, prefix="/api/v1/schedules", tags=["Schedules"])
app.include_router(milestones.router, prefix="/api/v1/milestones", tags=["Milestones"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])


