from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Clash(Base):
    __tablename__ = 'clashes'

    Id = Column(Integer, primary_key=True)
    TotalTime = Column(Integer, nullable=False)
    StartTime = Column(Integer, nullable=False)
    Result = Column(String(50), nullable=False)
    Game1_id = 
    Game2_id = 
    Level_id = Column(Integer, ForeignKey('levels.Id'))



Base.metadata.create_all(engine)