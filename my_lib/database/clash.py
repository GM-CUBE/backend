from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean
from datetime import datetime
from .base import Base

class Clash(Base):
    __tablename__ = 'clashes'

    Id = Column(Integer, primary_key=True)
    StartTime = Column(TIMESTAMP(), default=datetime.now())
    EndTime = Column(TIMESTAMP(), nullable=True)
    Result = Column(Boolean(), nullable=True)
    Level_id = Column(ForeignKey('levels.Id'))
    Game1_id = Column(ForeignKey('games.Id'))
    Game2_id = Column(ForeignKey('games.Id'))

    def serialize(self):
        return {
            "id": self.Id,
            "startTime": self.StartTime,
            "totalTime": self.EndTime,
            "result": self.Result,
            "level_id": self.Level_id,
            "game1_id": self.Game1_id,
            "game2_id": self.Game2_id
        }