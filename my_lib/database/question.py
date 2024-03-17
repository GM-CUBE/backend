from sqlalchemy import Column, ForeignKey, Integer, String, Float
from .base import Base

class Questions(Base):
    __tablename__ = 'questions'

    Id = Column(Integer(), primary_key=True)
    Question = Column(String(100), nullable=False)
    Time = Column(Float(), nullable=False)
    Level_id = Column(Integer, ForeignKey('levels.Id'))

    def serialize(self):
        return {
            "id": self.Id,
            "question": self.Question,
            "time": self.Time,
        }