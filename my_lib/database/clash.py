from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Clash(Base):
    __tablename__ = 'clashes'

    Id = Column(Integer, primary_key=True)
    TotalTime = Column(Integer, nullable=False)
    StartTime = Column(Integer, nullable=False)
    Result = Column(String(50), nullable=False)
    Game1_id = Column(Integer, ForeignKey('users.Id'))
    Game2_id = Column(Integer, ForeignKey('users.Id'))
    Level_id = Column(Integer, ForeignKey('levels.Id'))