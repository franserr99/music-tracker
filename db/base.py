from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
import os
from dotenv import load_dotenv

base = declarative_base()

def get_engine():
    load_dotenv("db.env")
    user=os.environ['user']
    pw=os.environ['password']
    port=os.environ['port']
    connector_str='mysql+mysqlconnector://'+user+':'+ pw+ '@localhost:'+ port+'/tracker'
    engine=create_engine(connector_str)
    return engine

engine = get_engine()
session_factory = sessionmaker(bind=engine)
ScopedSession = scoped_session(session_factory)