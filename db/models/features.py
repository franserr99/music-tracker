from sqlalchemy import Column, String, FLOAT, ForeignKey
from db.base import base

class Features(base):
    __tablename__ = 'Features'
    track_id = Column(String(100), ForeignKey('Library.uri'), unique=True, primary_key=True)
    danceability= Column(FLOAT)
    energy=Column(FLOAT)
    key=Column(FLOAT)
    loudness=Column(FLOAT)
    mode=Column(FLOAT)
    speechiness=Column(FLOAT)
    acousticness=Column(FLOAT)
    instrumentalness=Column(FLOAT)
    liveness=Column(FLOAT)
    valence=Column(FLOAT)
    tempo=Column(FLOAT)
