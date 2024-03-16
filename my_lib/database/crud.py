import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


engine = create_engine('postgresql://postgres:1234@localhost/GM_CUBE', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


TABLE_CLASS_MAP = {
    'activity': Activity,
    'clash': Clash,
    'example': Example,
    'game_question': Game_Question,
    'games': Games,
    'level': Level,
    'paragraph': Paragraph,
    'questions': Questions,
    'shortcut_game': Shortcut_Game,
    'shortcuts': Shortcuts,
    'user': Users
}


# --- Create -----------
def crate_table_row(table_name, row_info):
     table_class = TABLE_CLASS_MAP.get(table_name.lower())

     if table_class:
          row = table_class(**row_info)
          print(row)
          session.add(row)
          session.commit()

     else:
          print(f"No se encontró una clase correspondiente a la tabla {table_name}")
     


# --- Read -------------
def read_all_table(table_name):
     table_class = TABLE_CLASS_MAP.get(table_name.lower())

     if table_class:
          result = []
          data = session.query(table_class).all()
          for i in data:
               result.append(i.serialize())

          return result



def read_by_id(table_name, id):
     table_class = TABLE_CLASS_MAP.get(table_name.lower())

     if table_class:
          data = session.query(table_class).filter(table_class.Id == id).first()
          return data.serialize()



# --- Update -----------
def update_table_row(table_name, id, row_info):
     table_class = TABLE_CLASS_MAP.get(table_name.lower())

     if table_class:
          data = session.query(table_class).filter(table_class.Id == id).first()

          for key, value in row_info.items():
               setattr(data, key, value)
          session.commit()


# --- Delete -----------
def delete_table_row(table_name, id):
     table_class = TABLE_CLASS_MAP.get(table_name.lower())

     if table_class:
          try: 
               data = session.query(table_class).filter(table_class.Id == id).first()
               session.delete(data)
               session.commit()
          except:
               print('Not found')




# crate_Table('level', **{'Name': 'Bronce', 'MinimumPrestige': 0, 'MaximumPrestige': 100})