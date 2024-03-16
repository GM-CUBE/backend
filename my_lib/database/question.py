from sqlalchemy import Column, Integer, String, Text, Float
from .base import Base

class Questions(Base):
    __tablename__ = 'questions'

    Id = Column(Integer(), primary_key=True)
    Question = Column(Text(100), nullable=False)
    Answer = Column(String(50), nullable=False)
    Time = Column(Float(), nullable=False)
