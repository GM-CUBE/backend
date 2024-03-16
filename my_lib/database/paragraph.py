from sqlalchemy import Column, Integer, ForeignKey, String
from .base import Base

class Paragraph(Base):
     __tablename__ = 'paragraphs'

     Id = Column(Integer, primary_key=True)
     Information = Column(String(100), nullable=False) 
     Level_id = Column(ForeignKey('levels.Id'))

     def serialize(self):
          return {
               "id": self.Id,
               "information": self.Information,
               "level_id": self.Level_id
          }