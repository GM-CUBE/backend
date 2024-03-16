from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, ForeignKey

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Games(Base):
    __tablename__ = 'games'

    Id = Column(Integer(), primary_key=True)
    IdUser = Column(ForeignKey("users.Id"))
    Mistakes = Column(Integer(), nullable=False)
    Amount = Column(Integer(), nullable=False)

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)