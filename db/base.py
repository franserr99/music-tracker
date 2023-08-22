from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
import os
from dotenv import load_dotenv
from pathlib import Path
base = declarative_base()

def get_engine():
    # Use an absolute path to reference db.env
    env_path = Path(__file__).parent / "db.env"
    
    # Check if db.env exists
    if not env_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{env_path}'")
    if(load_dotenv(env_path,override=True)):
        print("atleast one set")
    else:
        print("none set")
    #print(os.environ)
    user=os.environ['user']
    pw=os.environ['password']
    port=os.environ['port']
    connector_str='mysql+mysqlconnector://'+user+':'+ pw+ '@localhost:'+ port+'/tracker'
    engine=create_engine(connector_str)
    return engine

engine = get_engine()
session_factory = sessionmaker(bind=engine)
ScopedSession = scoped_session(session_factory)