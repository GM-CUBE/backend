from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from .base import Base

class Game_Question(Base):
    __tablename__ = 'game_question'

    Id = Column(Integer, primary_key=True)
    Question = Column(ForeignKey("questions.Id"))
    Answer = Column(Integer(), nullable=False)
    Time = Column(Float(), nullable=False)
    Result = Column(Boolean(), nullable=False)
    Game_id = Column(ForeignKey("games.Id"))

    def serialize(self):
        return {
            "id": self.Id,
            "question": self.Question,
            "answer": self.Answer,
            "time": self.Time,
            "result": self.Result,
            "Game_id": self.Game_id
        }