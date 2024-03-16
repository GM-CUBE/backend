from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Example(Base):
    __tablename__ = 'examples'

    Id = Column(Integer, primary_key=True)
    Information = Column(String(120), nullable=False)
    Level_id = Column(Integer, ForeignKey('levels.Id'))



Base.metadata.create_all(engine)