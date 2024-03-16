from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Shortcuts(Base):
    __tablename__ = 'shortcuts'

    Id = Column(Integer(), primary_key=True)
    Name = Column(String(20), nullable=False)
    Weighing = Column(Float(), nullable=False)