from sqlalchemy import Column, String
from db.base import base

class Library(base):
    __tablename__ = 'Library'
    uri = Column(String(100), primary_key=True, unique=True)
    track_name = Column(String(100))
    track_artists = Column(String(100))
