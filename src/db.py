#Eduardo Ramos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import STR_DATABASE

engine = create_engine(STR_DATABASE, echo=True)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)

# To work with tables
Base = declarative_base()

# Creates, in case they don't exist, the tables of all models found in the application (imported)
async def criaTabelas():
    Base.metadata.create_all(engine)