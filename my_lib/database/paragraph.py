from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base


class Paragraph(Base):
     __tablename__ = 'paragraphs'

     Id = Column(Integer, primary_key=True)
     Information = Column(String(100), nullable=False) 
     Level_id = Column(Integer, ForeignKey('levels.id'))