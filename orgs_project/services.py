from sqlalchemy.orm import Session
from typing import List
from orgs_project.repositories import ActivityRepository, OrganizationRepository, BuildingRepository
from orgs_project.models import Activity, Organization, Building


class ActivityService:
    """Сервис для работы с деятельностями """
    
    def __init__(self, db: Session):
        self.repo = ActivityRepository(db)
    
    def get_all(self) -> List[Activity]:
        # Получить все деятельности
        return self.repo.get_all()
    
    def get_by_id(self, activity_id: int) -> Activity:
        # Получить деятельность по ID
        activity = self.repo.get_by_id(activity_id)
        if not activity:
            raise ValueError("Activity not found")
        return activity


class BuildingService:
    """Сервис для работы со зданиями"""
    
    def __init__(self, db: Session):
        self.repo = BuildingRepository(db)
        self.org_repo = OrganizationRepository(db)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Building]:
        # Получить все здания с пагинацией
        return self.repo.get_all(skip, limit)
    
    def get_by_id(self, building_id: int) -> Building:
        # Получить здание по ID
        building = self.repo.get_by_id(building_id)
        if not building:
            raise ValueError("Building not found")
        return building
    
    def get_organizations(self, building_id: int) -> List[Organization]:
        # Получить все организации в конкретном здании
        building = self.repo.get_by_id(building_id)
        if not building:
            raise ValueError("Building not found")
        return self.org_repo.get_by_building(building_id)


class OrganizationService:
    """Сервис для работы с организациями"""
    
    def __init__(self, db: Session):
        self.repo = OrganizationRepository(db)
        self.activity_repo = ActivityRepository(db)
        self.building_repo = BuildingRepository(db)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        # Получить все организации с пагинацией
        return self.repo.get_all(skip, limit)
    
    def get_by_id(self, organization_id: int) -> Organization:
        # Получить организацию по ID
        org = self.repo.get_by_id(organization_id)
        if not org:
            raise ValueError("Organization not found")
        return org
    
    def get_by_activity(self, activity_id: int) -> List[Organization]:
        # Найти все организации, связанные с деятельностью и поддеятельностями
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise ValueError("Activity not found")
        return self.repo.get_by_activity(activity_id)
    
    def search(self, query: str) -> List[Organization]:
        # Поиск организаций по названию
        if len(query) < 3:
            raise ValueError("Search query must be at least 3 characters")
        return self.repo.search_by_name(query)
    
    def get_nearby(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> List[Organization]:
        # Поиск организаций в прямоугольной области
        buildings = self.building_repo.get_by_coordinates_range(
            lat_min, lat_max, lon_min, lon_max)
        building_ids = [b.id for b in buildings]
        return self.repo.get_by_building_ids(building_ids)