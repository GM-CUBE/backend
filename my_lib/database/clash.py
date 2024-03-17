from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean
from datetime import datetime
from .base import Base

class Clash(Base):
    __tablename__ = 'clashes'

    Id = Column(Integer, primary_key=True)
    TotalTime = Column(Integer(), nullable=True)
    StartTime = Column(TIMESTAMP(), default=datetime.now())
    Result = Column(Boolean(), nullable=True)
    Level_id = Column(ForeignKey('levels.Id'))
    Game1_id = Column(ForeignKey('users.Id'))
    Game2_id = Column(ForeignKey('users.Id'))

    def serialize(self):
        return {
            "id": self.Id,
            "totalTime": self.TotalTime,
            "startTime": self.StartTime,
            "result": self.Result,
            "level_id": self.Level_id,
            "game1_id": self.Game1_id,
            "game2_id": self.Game2_id
        }