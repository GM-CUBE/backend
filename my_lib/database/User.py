from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, TIMESTAMP

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Users(Base):
    __tablename__ = 'users'

    Id = Column(Integer(), primary_key=True)
    FirstName = Column(String(20), nullable=False)
    LastName = Column(String(30), nullable=False)
    Age = Column(Integer(), nullable=False)
    Username = Column(String(15), nullable=False, unique=True)
    Password = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    EmailVerification = Column(TIMESTAMP(), nullable=False)
    Prestige = Column(Integer(), nullable=False)
    Coins = Column(Integer(), nullable=False)
    Strak = Column(Integer(), nullable=False)

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)