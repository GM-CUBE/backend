from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, ForeignKey

engine = create_engine('postgresql://<nombre>:@localhost/<basededatos>')

Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

class Shortcut_Game(Base):
    __tablename__ = 'shortcut_game'

    IdShortcut = Column(ForeignKey("shortcuts.Id"))
    IdGame = Column(ForeignKey("games.Id"))

if __name__ == '__main__':
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)