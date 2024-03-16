from sqlalchemy import Column, ForeignKey
from .base import Base

class Shortcut_Game(Base):
    __tablename__ = 'shortcut_game'

    IdShortcut = Column(ForeignKey("shortcuts.Id"))
    IdGame = Column(ForeignKey("games.Id"))
