from sqlalchemy import Column, Integer, ForeignKey
from .base import Base


class Activity(Base):
    __tablename__ = 'activities'

    Id = Column(Integer, primary_key=True)
    Level_id = Column(Integer, ForeignKey('levels.Id'))
    Questions = Column(ForeignKey('questions.Id'))

    def serialize(self):
        return {
            "id": self.Id,
            "level_id": self.Level_id,
            "questions": self.Questions
        }