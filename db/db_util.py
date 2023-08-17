from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import  sqlalchemy, spotipy, datetime, pytz
from sqlalchemy import create_engine, Column, String, ForeignKey, DateTime, FLOAT, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

class history_util:
    @staticmethod
    def push_history_data(records:tuple, term:str, id:str,engine: sqlalchemy.engine.Engine): #an example of expected tuple:near_term= (track_idx,tracks_name,artist_names)
        assert( term=='short_term' or term=='medium_term' or term=='long_term' )
        #recall: the history table has the following fields: user_id, date_recorded, relative_term, track_id
        track_idx= records[0] #list of track ids
        tracks_name= records[1] #list of corresponding track names
        artist_names=records[2] #list of corresponding artist names
        now= datetime.datetime.now(pytz.timezone('US/Pacific')) #the timestamp used for all the records we are going to push right now 
        assert(len(track_idx)==len(tracks_name)==len(artist_names))
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()
        class users(base): 
            __tablename__='users'
            id = Column(String(50), primary_key=True, unique=True)
        class track_library(base):
            __tablename__='library'
            uri= Column(String(26),primary_key=True, unique=True)
            track_name=Column(String(100))
            track_artists=Column(String(100))
        class listening_history(base):
            __tablename__='history'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime)
            relative_term=Column(String(30), primary_key=True)
            track_id= Column (String(26) , ForeignKey('library.uri'), primary_key=True, unique=False)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id'),)
        try:
            if (term=="long_term") :
                three_months_ago=(now-datetime.timedelta(3*30)).astimezone(pytz.timezone('US/Pacific'))
                history=session.query(listening_history).filter(id==listening_history.user_id).filter(listening_history.relative_term=="long_term").all()
                
                for record in history:
                    recorded_date_tz=datetime.datetime.replace(record.date_recorded, tzinfo=pytz.timezone('US/Pacific'))
                    if recorded_date_tz>three_months_ago:
                        print("longterm recorded within the last three months already happeend")
                        return
            if(term=="medium_term"):
                two_months_ago=(now-datetime.timedelta(2*30)).astimezone(pytz.timezone('US/Pacific'))
                history=session.query(listening_history).filter(id==listening_history.user_id).filter(listening_history.relative_term=="medium_term").all()
                for record in history:
                    recorded_date_tz=datetime.datetime.replace(record.date_recorded, tzinfo=pytz.timezone('US/Pacific'))
                    if recorded_date_tz>two_months_ago:
                        print("midterm recorded within the last two months already happeend")
                        return
            if(term=="short_term"):
                month_ago=(now-datetime.timedelta(30)).astimezone(pytz.timezone('US/Pacific'))
                day_ago=(now-datetime.timedelta(1)).astimezone(pytz.timezone('US/Pacific'))
                history=session.query(listening_history).filter(id==listening_history.user_id).filter(listening_history.relative_term=="short_term").all()
                for record in history:
                    recorded_date_tz=datetime.datetime.replace(record.date_recorded, tzinfo=pytz.timezone('US/Pacific'))
                    if recorded_date_tz>month_ago or recorded_date_tz>day_ago:
                        print("short recorded within the last month already happeend")
                        return
            for track_ID  in track_idx :
                session.add(listening_history(user_id=id, date_recorded= now, relative_term=term, track_id= track_ID))
                session.commit()
        finally:
            session.close()   
    @staticmethod
    def get_listening_history(engine: sqlalchemy.engine.Engine, music_id:str): 
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()
        #make model that represents the table
        class users(base): #keep a high level users table in order to expand this another way if you want to later
            __tablename__='users'
            id = Column(String(50), primary_key=True, unique=True)
        class track_library(base):
            __tablename__='library'
            uri= Column(String(26),primary_key=True, unique=True)
            track_name=Column(String(100))
            track_artists=Column(String(100))
        class listening_history(base):
            __tablename__='history'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime)
            relative_term=Column(String(30), primary_key=True)
            track_id= Column (String(26) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id'),)
        try:
            history=session.query(listening_history).filter(listening_history.user_id==music_id).all()
            return history
        finally:
            session.close()
    @staticmethod
    def get_listening_history_by_term(engine: sqlalchemy.engine.Engine, music_id:str, term:str): 
        assert(term==('short_term' or 'middle_term' or 'long_term' ))
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        session = Session()
        #make model that represents the table
        class users(base):
            __tablename__='users'
            id = Column(String(50), primary_key=True, unique=True)
        class track_library(base):
            __tablename__='library'
            uri= Column(String(26),primary_key=True, unique=True)
            track_name=Column(String(100))
            track_artists=Column(String(100))
        class listening_history(base):
            __tablename__='history'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime)
            relative_term=Column(String(30), primary_key=True)
            track_id= Column (String(26) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'relative_term', 'track_id'),)
        try:
            history=session.query(listening_history).filter(listening_history.user_id==music_id).filter(listening_history.relative_term).all()
            return history
        finally:
            session.close()
    @staticmethod
    def get_most_recent_history(): 
        pass
    @staticmethod
    def get_songs_heard(engine: sqlalchemy.engine.Engine):
        pass

class rec_util:
    @staticmethod
    def get_potential_recs(user_ID:str, engine: sqlalchemy.engine.Engine):
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        class potential_recs(base):
            __tablename__='potential_recs'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()
        try:
            recs=session.query(potential_recs).filter(potential_recs.user_id==user_ID).all()
            rec_IDs=[]
            for rec in recs:
                if(rec.track_id not in rec_IDs):
                    rec_IDs.append(rec.track_id)
            return rec_IDs
        finally:
            session.close()
    @staticmethod
    def latest_record_date(engine: sqlalchemy.engine.Engine, user_ID:str):
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        #returns the last time a record was pushed for this user 
        class potential_recs(base):
            __tablename__='potential_recs'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()

        try: 
            recs= session.query(potential_recs).filter(potential_recs.track_id==user_ID)
            earliest=recs[0].date_recorded
            for rec in recs:
                if rec.date_recorded> earliest:
                    earliest= rec.date_recorded
            return earliest
        finally:
            session.close()



    @staticmethod
    def push_pontential_recs(engine: sqlalchemy.engine.Engine, track_IDs:list, user:str):
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        
        class potential_recs(base):
            __tablename__='potential_recs'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()
        now= datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S') #the timestamp used for all the records we are going to push right now 
        try:
            db_recs_for_user=rec_util.get_potential_recs(user_ID=user,engine=engine)
            for track in track_IDs:
                if track not in db_recs_for_user:
                    session.add(potential_recs(user_id=user, date_recorded=now, track_id=track))
                    session.commit()
        finally:
            session.close()
        
class seed_util:
    @staticmethod
    def get_stored_seeds(user_ID:str, engine: sqlalchemy.engine.Engine):
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        class seed_tracks(base):
            __tablename__='seed_tracks'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()
        try:
            recs=session.query(seed_tracks).filter(seed_tracks.user_id==user_ID).all()
            seed_IDs=[]
            for rec in recs:
                if(rec.track_id not in seed_IDs):
                    seed_IDs.append(rec.track_id)
            return seed_IDs
        finally:
            session.close()
    @staticmethod
    def latest_record_date(engine: sqlalchemy.engine.Engine,user_ID:str):
        #returns the last time a record was pushed for this user 
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        class seed_tracks(base):
            __tablename__='seed_tracks'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()
        try: 
            recs= session.query(seed_tracks).filter(seed_tracks.track_id==user_ID)
            earliest=recs[0].date_recorded
            for rec in recs:
                if rec.date_recorded> earliest:
                    earliest= rec.date_recorded
            return earliest
        finally:
            session.close()
    @staticmethod
    def push_seeds(engine: sqlalchemy.engine.Engine,  track_IDs:list, user:str):
        base=declarative_base()
        Session = sessionmaker(bind=engine)
        class seed_tracks(base):
            __tablename__='seed_tracks'
            user_id = Column(String(50),ForeignKey('users.id'), primary_key=True)
            date_recorded=Column(DateTime, primary_key=True)
            track_id= Column (String(100) , ForeignKey('library.uri'), primary_key=True)
            __table_args__ = (PrimaryKeyConstraint('user_id', 'track_id', 'date_recorded'),)
        session=Session()
        now= datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
        #the timestamp used for all the records we are going to push right now 
        try:
            db_recs_for_user=seed_util.get_stored_seeds(user_ID=user,engine=engine)
            for track in track_IDs:
                if track not in db_recs_for_user:
                    session.add(seed_tracks(user_id=user, date_recorded=now, track_id=track))
                    session.commit()
        finally:
            session.close()

class artist_util:
    @staticmethod
    def get_listened_artists(engine: sqlalchemy.engine.Engine,user_id:str ): 
        all_artists=[]
        song_names, song_artists= song_util.get_song_info()



        for song_artist in song_artists:
            artists=song_artist.split(",")
            for creator in artists:
                cre=str(creator.strip())
                if cre not in all_artists: #the list as a value for the key:value pairing does not exist yet
                    all_artists.append(cre)
        return all_artists