from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from orgs_project.core.database import get_db
from orgs_project.services import ActivityService, OrganizationService
from orgs_project.schemas import Activity, Organization

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("/", response_model=List[Activity])
def get_activities(
    db: Session = Depends(get_db)
):
    service = ActivityService(db)
    return service.get_all()


@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    service = ActivityService(db)
    try:
        return service.get_by_id(activity_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/{activity_id}/organizations/", response_model=List[Organization])
def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    try:
        return service.get_by_activity(activity_id)
    except ValueError as e:
        raise HTTPException(404, str(e))