from sqlalchemy import Column, String
from db.base import base

class User(base): 
    #keep a high level users table in order to expand this another way if you want to later
    __tablename__='User'
    id = Column(String(50), unique=True, primary_key=True)
