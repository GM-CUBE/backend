from sqlalchemy import Column, ForeignKey, Integer
from .base import Base

class Shortcut_Game(Base):
    __tablename__ = 'shortcut_game'

    Id = Column(Integer(), primary_key=True)
    IdShortcut = Column(ForeignKey("shortcuts.Id"))
    Game_id = Column(ForeignKey("games.Id"))

    def serialize(self):
        return {
            "id": self.Id,
            "idShortcut": self.IdShortcut,
            "game_id": self.Game_id
        }