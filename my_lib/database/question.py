from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Questions(Base):
    __tablename__ = 'questions'

    Id = Column(Integer(), primary_key=True)
    Question = Column(String(100), nullable=False)
    Answer = Column(String(50), nullable=False)
    Time = Column(Float(), nullable=False)

    def serialize(self):
        return {
            "id": self.Id,
            "questions": self.Question,
            "answer": self.Answer,
            "time": self.Time
        }