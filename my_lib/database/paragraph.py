from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Paragraph(Base):
     __tablename__ = 'paragraphs'

     Id = Column(Integer, primary_key=True)
     Information = Column(String(100), nullable=False) 
     Level_id = Column(Integer, ForeignKey('levels.id'))


Base.metadata.create_all(engine)