from sqlalchemy import Column, ForeignKey
from .base import Base

class Clash_Question(Base):
    __tablename__ = 'clash_questions'

    Clash_Id = Column(ForeignKey("clash.Id"), primary_key=True)
    Question_Id = Column(ForeignKey("question.Id"))

    def serialize(self):
        return {
            "clash_id": self.Question_Id,
            "question_id": self.Clash_Id
        }