from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

engine = create_engine('postgresql://', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)