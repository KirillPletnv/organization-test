import pytest
from fastapi.testclient import TestClient
from orgs_project.main import app
from orgs_project.core.config import settings

client = TestClient(app)

def test_api_key_required():
    """Доступ без ключа запрещён"""
    response = client.get("/buildings/")
    assert response.status_code == 403

def test_buildings_list():
    """Список зданий должен содержать 5 записей"""
    response = client.get(
        "/buildings/",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["address"] == "ул. Ленина 1, Москва"

def test_building_by_id():
    """Здание с ID=1 ул. Ленина"""
    response = client.get(
        "/buildings/1",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == "ул. Ленина 1, Москва"
    assert data["latitude"] == 55.7558

def test_organizations_in_building():
    """В здании 1 должны быть только 'Мясной двор'"""
    response = client.get(
        "/buildings/1/organizations",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Мясной двор"

def test_activities_list():
    """Должно быть 10 деятельностей"""
    response = client.get(
        "/activities/",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert data[0]["name"] == "Еда"

def test_organizations_by_activity_1():
    """По деятельности 'Еда' (id=1) должны найтись 3 организации"""
    response = client.get(
        "/activities/1/organizations/",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    names = [org["name"] for org in data]
    assert "Мясной двор" in names
    assert "Сыроварня" in names
    assert "Универсальный магазин" in names


def test_organizations_by_activity_2():
    """По деятельности 'Автомобили' (id=2) должны найтись 2 организации"""
    response = client.get(
        "/activities/2/organizations/",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  
    
    names = [org["name"] for org in data]
    assert "Автосалон" in names
    assert "Автозапчасти" in names


def test_organizations_list():
    """Всего должно быть 5 организаций"""
    response = client.get(
        "/organizations/",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_organization_by_id_1():
    """Организация с ID=1 должна быть 'Мясной двор' с правильными телефонами"""
    response = client.get(
        "/organizations/1",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Мясной двор"
    assert len(data["phone_numbers"]) == 2
    assert "+7-495-123-45-67" in data["phone_numbers"]
    

    act_names = [a["name"] for a in data["activities"]]
    assert "Мясная продукция" in act_names
    assert "Колбасные изделия" in act_names

def test_search_organizations():
    """Поиск по 'Мясной' должен найти 'Мясной двор'"""
    response = client.get(
        "/organizations/search/?q=%D0%9C%D1%8F%D1%81%D0%BD%D0%BE%D0%B9",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Мясной двор"

def test_organizations_nearby():
    """В прямоугольнике вокруг центра должны найтись все 5 организаций"""
    response = client.get(
        "/organizations/nearby/?lat_min=55.70&lat_max=55.80&lon_min=37.50&lon_max=37.70",
        headers={"X-API-Key": settings.API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
