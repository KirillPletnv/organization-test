from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from orgs_project.core.database import get_db
from orgs_project.services import BuildingService
from orgs_project.schemas import Building, Organization

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[Building])
def get_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = BuildingService(db)
    return service.get_all(skip, limit)


@router.get("/{building_id}", response_model=Building)
def get_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    service = BuildingService(db)
    try:
        return service.get_by_id(building_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/{building_id}/organizations", response_model=List[Organization])
def get_organizations_in_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    service = BuildingService(db)
    try:
        return service.get_organizations(building_id)
    except ValueError as e:
        raise HTTPException(404, str(e))