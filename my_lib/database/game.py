from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Games(Base):
    __tablename__ = 'games'

    Id = Column(Integer(), primary_key=True)
    IdUser = Column(ForeignKey("users.Id"))
    Mistakes = Column(Integer(), nullable=False)
    Amount = Column(Integer(), nullable=False)
