from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Level(Base):
    __tablename__ = 'levels'

    Id = Column(Integer(), primary_key=True)
    Name = Column(String(50), nullable=False, unique=True)
    MinimumPrestige = Column(Integer(), nullable=False)
    MaximumPrestige = Column(Integer(), nullable=False)
    
    def serialize(self):
        return {
            "id": self.Id,
            "name": self.Name,
            "minimumPrestige": self.MinimumPrestige,
            "maximumPrestige": self.MaximumPrestige
        }