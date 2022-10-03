from enum import unique
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

def get_session():
    #connect with data base
    engine = create_engine('sqlite:////home/yusufkaya/vs/1crossover/sqlalchemy_5.sqlite')
    factory = sessionmaker(bind=engine)
    session = scoped_session(factory)
    return session

# manage tables
base= declarative_base()

class Crossover_project(base):  

    __tablename__ = 'Crossover_project' #DB'de oluşturdugumuz tablonun adi ve kolonlari.
    id = Column(Integer, primary_key=True,autoincrement="auto")
    ip = Column(String)
    user = Column(String)
    password = Column(String)
    mail = Column(String)
    cpu = Column(String)
    RAMmemory = Column(String)
    
    
engine = create_engine('sqlite:////home/yusufkaya/vs/1crossover/sqlalchemy_5.sqlite')
base.metadata.create_all(engine)
