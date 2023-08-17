from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, FLOAT, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def main():
    load_dotenv("../db.env")
    user=os.environ['user']
    pw=os.environ['password']
    port=os.environ['port']
    connector_str='mysql+mysqlconnector://'+user+':'+pw+'@localhost:'+ port+'/music-tracker'
    engine=create_engine(connector_str)
    base=declarative_base()

    #the column names are inferred from the variable names 
    class Library(base):
        __tablename__='Library'
        uri= Column(String(100),primary_key=True, unique=True)
        track_name=Column(String(100))
        track_artists=Column(String(100))
    class Features(base):
        __tablename__='Features'
        #example audiofeature 
        #danceability': 0.232, 'energy': 0.441, 'key': 10, 'loudness': -14.604, 'mode': 1, 
        #'speechiness': 0.0452, 'acousticness': 0.135, 'instrumentalness': 0.0441, 'liveness': 0.668,
        #'valence': 0.237, 'tempo': 147.655
        track_id = Column(String(100), ForeignKey('Library.uri'), unique=True,primary_key=True )
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
    #listening history, when we know they have heard a song
    class History(base):
        __tablename__='History'
        user_id = Column(String(50),ForeignKey('User.id'))
        date_recorded=Column(DateTime)
        relative_term=Column(String(30))
        track_id= Column (String(100) , ForeignKey('Library.uri'))
        __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id', 'date_recorded'),)
    #when we pull from their top tracks 
    class TopTrack(base):
        __tablename__='TopTrack'
        user_id = Column(String(50),ForeignKey('User.id'))
        date_recorded=Column(DateTime)
        relative_term=Column(String(30))
        track_id= Column (String(100) , ForeignKey('Library.uri'))
        __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id', 'date_recorded'),)
    #songs they liked in playlists they did not create
    class Liked(base):
        __tablename__='Liked'
        user_id = Column(String(50),ForeignKey('User.id'))
        track_id= Column (String(100), ForeignKey('Library.uri'))
        source=Column(String(20))
        __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id','source'),)
    class User(base): 
        #keep a high level users table in order to expand this another way if you want to later
        __tablename__='User'
        id = Column(String(50), unique=True, primary_key=True)
    #create tables
    base.metadata.create_all(bind=engine)
    #create session
    Session = sessionmaker(bind=engine)
    session = Session()

if __name__ == "__main__":
    main()

