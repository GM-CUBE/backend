from sqlalchemy import Column, Integer, ForeignKey
from .base import Base


class Activity(Base):
    __tablename__ = 'activities'

    Id = Column(Integer, primary_key=True)
    Level_id = Column(Integer, ForeignKey('levels.Id'))
    Questions = Column(Integer, ForeignKey('questions.Id'))