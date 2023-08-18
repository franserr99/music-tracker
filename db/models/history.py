from sqlalchemy import Column, String, ForeignKey,DateTime,PrimaryKeyConstraint
from db.base import base

class History(base):
    __tablename__='History'
    user_id = Column(String(50),ForeignKey('User.id'))
    date_recorded=Column(DateTime)
    relative_term=Column(String(30))
    track_id= Column (String(100) , ForeignKey('Library.uri'))
    __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id', 'date_recorded'),)
