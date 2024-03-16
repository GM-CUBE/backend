from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Games(Base):
    __tablename__ = 'games'

    Id = Column(Integer(), primary_key=True)
    Amount = Column(Integer(), nullable=False)
    Mistakes = Column(Integer(), nullable=False)
    User_id = Column(ForeignKey("users.Id"))

    def serialize(self):
        return {
            "id": self.Id,
            "amount": self.Amount,
            "mistakes": self.Mistakes,
            "User_id": self.User_id
        }