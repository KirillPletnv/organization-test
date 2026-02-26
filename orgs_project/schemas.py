from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List


class Building(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    
    model_config = {"from_attributes": True}


class Activity(BaseModel):
    id: int
    name: str
    
    model_config = {"from_attributes": True}



class Organization(BaseModel):
    id: int
    name: str
    building_id: int
    phone_numbers: List[str] = []
    building: Optional[Building] = None
    activities: List[Activity] = []
    
    model_config = {"from_attributes": True}


