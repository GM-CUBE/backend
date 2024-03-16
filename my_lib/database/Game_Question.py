from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Game_Question(Base):
    __tablename__ = 'game_question'

    IdQuestion = Column(ForeignKey("questions.Id"))
    IdGame = Column(ForeignKey("games.Id"))
    Time = Column(Float(), nullable=False)
    Answer = Column(Integer(), nullable=False)
    Result = Column(Boolean(), nullable=False)

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)