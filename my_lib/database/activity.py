from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Activity(Base):
    __tablename__ = 'activities'

    Id = Column(Integer, primary_key=True)
    Level_id = Column(Integer, ForeignKey('levels.Id'))
    Questions = 



Base.metadata.create_all(engine)