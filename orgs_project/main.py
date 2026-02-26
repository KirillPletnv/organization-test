from fastapi import FastAPI, Depends
from .api.v1 import buildings, organizations, activities
from orgs_project.core.security import verify_api_key

from orgs_project.core.config import settings
print("🔥 REAL API_KEY:", settings.API_KEY)

app = FastAPI(title="Organization Directory")

app.include_router(buildings.router, dependencies=[Depends(verify_api_key)])
app.include_router(organizations.router, dependencies=[Depends(verify_api_key)])
app.include_router(activities.router, dependencies=[Depends(verify_api_key)])


@app.get("/")
def root():
    return {"message": "Organization Directory API"}

