from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from .core.database import Base


class Building(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)    
    
    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    organizations = relationship("Organization", secondary="organization_activity", back_populates="activities")
    



organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id"))
)


class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_numbers = Column(JSON, default=list, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    
    building = relationship("Building", back_populates="organizations") 
    activities = relationship("Activity", secondary="organization_activity", back_populates="organizations")