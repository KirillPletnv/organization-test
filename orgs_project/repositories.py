from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from orgs_project.models import Building, Organization, Activity, organization_activity


class BaseRepository:
    """Базовый репозиторий """
    
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: int):
        # Получить запись по ID
        return self.db.get(self.model, id)
    
    def get_all(self, skip: int = 0, limit: int = 100):
        # Получить все записи с пагинацией
        return self.db.query(self.model).offset(skip).limit(limit).all()


class BuildingRepository(BaseRepository):
    """Репозиторий для работы со зданиями"""
    
    def __init__(self, db: Session):
        super().__init__(db, Building)
    
    def get_by_coordinates_range(self, lat_min, lat_max, lon_min, lon_max):
        # Найти здания в прямоугольной области по координатам
        return self.db.query(Building).filter(
            Building.latitude.between(lat_min, lat_max),
            Building.longitude.between(lon_min, lon_max)
        ).all()


class ActivityRepository:
    """Репозиторий для работы с деятельностями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, activity_id: int) -> Optional[Activity]:
        # Получить деятельность по ID
        return self.db.get(Activity, activity_id)
    
    def get_all(self) -> List[Activity]:
        # Получить все деятельности
        return self.db.query(Activity).all()
    
    def get_descendants(self, activity_id: int) -> List[int]:
        """Рекурсивно собирает всех потомков"""
        query = text("""
            WITH RECURSIVE activity_tree AS (
                SELECT id FROM activities WHERE id = :aid
                UNION ALL
                SELECT a.id FROM activities a
                JOIN activity_tree at ON a.parent_id = at.id
            )
            SELECT id FROM activity_tree
        """)
        result = self.db.execute(query, {"aid": activity_id})
        return [row[0] for row in result]


class OrganizationRepository(BaseRepository):
    """Репозиторий для работы с организациями"""
    
    def __init__(self, db: Session):
        super().__init__(db, Organization)

    def get_by_building(self, building_id: int):
        # Найти все организации в конкретном здании
        return self.db.query(Organization).filter(
            Organization.building_id == building_id).all()
    
    def get_by_building_ids(self, building_ids: List[int]):
        # Найти все организации в списке зданий
        return self.db.query(Organization).filter(
            Organization.building_id.in_(building_ids)).all()
    
    def get_by_activity(self, activity_id: int):
        # Найти все организации по деятельности 
        activity_repo = ActivityRepository(self.db)
        all_ids = activity_repo.get_descendants(activity_id)        
        if not all_ids:
            return []       
        org_ids_result = self.db.execute(
            text("SELECT DISTINCT organization_id FROM organization_activity WHERE activity_id IN :ids"),
            {"ids": tuple(all_ids)})
        org_ids = [row[0] for row in org_ids_result]       
        if not org_ids:
            return []        
        return self.db.query(Organization).filter(Organization.id.in_(org_ids)).all()
    
    def search_by_name(self, query: str):
        # Поиск организаций по названию (частичное совпадение)
        return self.db.query(Organization).filter(
            Organization.name.ilike(f"%{query}%")).all()
        