from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://', echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Level(Base):
    __tablename__ = 'levels'

    Id = Column(Integer, primary_key=True)
    Name = Column(String(50), nullable=False, unique=True)
    MinimumPrestige = Column(Integer, nullable=False)
    MaximumPrestige = Column(Integer, nullable=False)

    Paragraphs = relationship('Paragraph', backref='level')
    Examples = relationship('Example', backref='level')
    Activities = relationship('Activity', backref='level')
    Clashes = relationship('Clash', backref='level')


Base.metadata.create_all(engine)