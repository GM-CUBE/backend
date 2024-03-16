from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Example(Base):
    __tablename__ = 'examples'

    Id = Column(Integer, primary_key=True)
    Information = Column(String(120), nullable=False)
    Level_id = Column(Integer, ForeignKey('levels.Id'))