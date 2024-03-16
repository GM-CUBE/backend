from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Shortcuts(Base):
    __tablename__ = 'shortcuts'

    Id = Column(Integer(), primary_key=True)
    Name = Column(String(20), nullable=False)
    Weighing = Column(Float(), nullable=False)

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)