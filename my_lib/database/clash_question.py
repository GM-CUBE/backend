from sqlalchemy import Column, ForeignKey, Integer
from .base import Base

class Clash_Question(Base):
    __tablename__ = 'clash_questions'

    Id = Column(Integer(), primary_key=True)
    Clash_Id = Column(ForeignKey("clashes.Id"))
    Question_Id = Column(ForeignKey("questions.Id"))

    def serialize(self):
        return {
            "clash_id": self.Question_Id,
            "question_id": self.Clash_Id
        }