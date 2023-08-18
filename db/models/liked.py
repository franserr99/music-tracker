from sqlalchemy import Column, String, ForeignKey,PrimaryKeyConstraint
from db.base import base

class Liked(base):
    __tablename__='Liked'
    user_id = Column(String(50),ForeignKey('User.id'))
    track_id= Column (String(100), ForeignKey('Library.uri'))
    source=Column(String(20))
    __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id','source'),)
