from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from orgs_project.core.database import get_db
from orgs_project.services import OrganizationService
from orgs_project.schemas import Organization

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=List[Organization])
def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    return service.get_all(skip, limit)


@router.get("/nearby/", response_model=List[Organization])
def get_organizations_nearby(
    lat_min: float = Query(...),
    lat_max: float = Query(...),
    lon_min: float = Query(...),
    lon_max: float = Query(...),
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    return service.get_nearby(lat_min, lat_max, lon_min, lon_max)

@router.get("/search/", response_model=List[Organization])
def search_organizations(
    q: str = Query(..., min_length=3),
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    try:
        return service.search(q)
    except ValueError as e:
        raise HTTPException(400, str(e))



@router.get("/{organization_id}", response_model=Organization)
def get_organization(
    organization_id: int,
    db: Session = Depends(get_db)
):
    service = OrganizationService(db)
    try:
        return service.get_by_id(organization_id)
    except ValueError as e:
        raise HTTPException(404, str(e))



