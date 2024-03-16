from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from .base import Base

class Game_Question(Base):
    __tablename__ = 'game_question'

    IdQuestion = Column(ForeignKey("questions.Id"))
    IdGame = Column(ForeignKey("games.Id"))
    Time = Column(Float(), nullable=False)
    Answer = Column(Integer(), nullable=False)
    Result = Column(Boolean(), nullable=False)
