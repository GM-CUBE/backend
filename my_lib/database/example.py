from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Example(Base):
    __tablename__ = 'examples'

    Id = Column(Integer, primary_key=True)
    Information = Column(String(120), nullable=False)
    Level_id = Column(ForeignKey('levels.Id'))

    def serialize(self):
        return {
            "id": self.Id,
            "information": self.Information,
            "level_id": self.Level_id
        }