from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

from .activity import Activity
from .clash import Clash
from .example import Example
from .game_question import Game_Question
from .game import Games
from .paragraph import Paragraph
from .question import Questions
from .shortcut_game import Shortcut_Game
from .shortcut import Shortcuts
from .user import Users
from .level import Level

from .crud import crate_table_row, read_all_table, update_table_row, delete_table_row

engine = create_engine('postgresql://postgres:1234@localhost:5432/GM_CUBE', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)