from sqlalchemy import Column, Integer, String, TIMESTAMP
from .base import Base

class Users(Base):
    __tablename__ = 'users'

    Id = Column(Integer(), primary_key=True)
    FirstName = Column(String(20), nullable=False)
    LastName = Column(String(30), nullable=False)
    Age = Column(Integer(), nullable=False)
    Username = Column(String(15), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    EmailVerification = Column(TIMESTAMP())
    Prestige = Column(Integer(), nullable=False)
    Coins = Column(Integer(), nullable=False)
    Streak = Column(Integer(), nullable=False)
