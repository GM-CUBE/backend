from sqlalchemy import Column, Integer, String, Float
from .base import Base

class Shortcuts(Base):
    __tablename__ = 'shortcuts'

    Id = Column(Integer(), primary_key=True)
    Price = Column(Integer())
    Name = Column(String(20), nullable=False)
    Weighing = Column(Float(), nullable=False)

    def serialize(self):
        return {
            "id": self.Id,
            "price": self.Price,
            "name": self.Name,
            "weighing": self.Weighing
        }