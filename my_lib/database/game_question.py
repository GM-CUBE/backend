from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from .base import Base

class Game_Question(Base):
    __tablename__ = 'game_question'

    Id = Column(Integer(), primary_key=True)
    Answer = Column(String(512), nullable=False)
    Time = Column(Integer(), nullable=False)
    Result = Column(Boolean(), nullable=False)
    Question = Column(ForeignKey("questions.Id"))
    Game_id = Column(ForeignKey("games.Id"))

    def serialize(self):
        return {
            "id": self.Id,
            "answer": self.Answer,
            "time": self.Time,
            "result": self.Result,
            "question_id": self.Question,
            "game_id": self.Game_id
        }