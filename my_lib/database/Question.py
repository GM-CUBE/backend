from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, Float

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Questions(Base):
    __tablename__ = 'questions'

    Id = Column(Integer(), primary_key=True)
    Question = Column(Text(100), nullable=False)
    Answer = Column(String(50), nullable=False)
    Time = Column(Float(), nullable=False)

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)