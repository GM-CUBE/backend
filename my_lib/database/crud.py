from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

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

from .base import Base

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

class DB_interface:
     def __init__(self) -> None:
          db_url = os.getenv('DB_URL')
          db_name = os.getenv('DB_NAME')
          db_user = os.getenv('DB_USER')
          db_password = os.getenv('DB_PASSWORD')
          db_type = os.getenv('DB_TYPE')
          db_container_name = os.getenv('DB_CONTAINER_NAME')
          
          self.db_url = ''

          if db_url != '':
               self.db_url = db_url
          else:
               if db_type == '0':
                    self.db_url = f"postgresql://{db_user}:{db_password}@localhost/{db_name}"
               elif db_type == '1':
                    self.db_url = f"postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}"


          self.engine = create_engine(self.db_url, echo=False)

          Session = sessionmaker(bind=self.engine)
          
          self.session = Session()

          Base.metadata.create_all(self.engine)


     # --- Create -----------
     def crate_table_row(self, table_name, row_info):
          table_class = TABLE_CLASS_MAP.get(table_name.lower())

          if table_class:
               row = table_class(**row_info)
               print(row)
               self.session.add(row)
               self.session.commit()

          else:
               print(f"No se encontró una clase correspondiente a la tabla {table_name}")
          


     # --- Read -------------
     def read_all_table(self, table_name):
          table_class = TABLE_CLASS_MAP.get(table_name.lower())

          if table_class:
               result = []
               data = self.session.query(table_class).all()
               for i in data:
                    result.append(i.serialize())

               return result



     def read_by_id(self, table_name, id):
          table_class = TABLE_CLASS_MAP.get(table_name.lower())

          if table_class:
               data = self.session.query(table_class).filter(table_class.Id == id).first()
               return data.serialize()



     # --- Update -----------
     def update_table_row(self, table_name, id, row_info):
          table_class = TABLE_CLASS_MAP.get(table_name.lower())

          if table_class:
               data = self.session.query(table_class).filter(table_class.Id == id).first()

               for key, value in row_info.items():
                    setattr(data, key, value)
               self.session.commit()


     # --- Delete -----------
     def delete_table_row(self, table_name, id):
          table_class = TABLE_CLASS_MAP.get(table_name.lower())

          if table_class:
               try: 
                    data = self.session.query(table_class).filter(table_class.Id == id).first()
                    self.session.delete(data)
                    self.session.commit()
               except:
                    print('Not found')




# crate_Table('level', **{'Name': 'Bronce', 'MinimumPrestige': 0, 'MaximumPrestige': 100})