from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Queue(Base):
    __tablename__ = 'queue'

    Id = Column(Integer(), primary_key=True)
    IdUser = Column(Integer(), ForeignKey('users.Id'))
    Prestige = Column(Integer(), nullable=False)