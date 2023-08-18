import   datetime, pytz
from db.base import ScopedSession
from db.models.history import History
from db.models.liked import Liked
from db.queries.user_queries import user_id_list,create_user
from db.queries.library_queries import get_song_info

class recs:
    @staticmethod
    def get_potential_recs(user_ID:str, ):
        session=ScopedSession()
        try:
            recs=session.query(Liked).filter(Liked.user_id==user_ID).all()
            rec_IDs=[]
            for rec in recs:
                if(rec.track_id not in rec_IDs):
                    rec_IDs.append(rec.track_id)
            return rec_IDs
        finally:
            session.close()
    @staticmethod
    def latest_record_date( user_ID:str):
        #returns the last time a record was pushed for this user 
        
        session=ScopedSession()

        try: 
            recs= session.query(Liked).filter(Liked.track_id==user_ID)
            earliest=recs[0].date_recorded
            for rec in recs:
                if rec.date_recorded> earliest:
                    earliest= rec.date_recorded
            return earliest
        finally:
            session.close()
    @staticmethod
    def push_pontential_recs( track_IDs:list, user:str):
        session=ScopedSession()
        now= datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S') #the timestamp used for all the records we are going to push right now 
        try:
            db_recs_for_user=recs.get_potential_recs(user_ID=user)
            for track in track_IDs:
                if track not in db_recs_for_user:
                    session.add(recs.potential_recs(user_id=user, date_recorded=now, track_id=track))
            session.commit()
        finally:
            session.close()
        
class seeds:
    @staticmethod
    def get_fav_songs_uri(user:str):
        all_users= user_id_list()
        if user not in all_users:
            create_user(id=user)
            print("user not in databse, tracks from history to get ")
            return
        try:
            session=ScopedSession()   
            user_listening_hist=session.query(History).filter(History.user_id==user).all()
            unique_track_uri=[]
            for track_listenened in user_listening_hist:
                if track_listenened.uri not in unique_track_uri:
                    unique_track_uri.append(track_listenened.uri)
            return unique_track_uri
        finally:
            session.close()
    @staticmethod
    def fav_songs_info( user_id:str):
        song_uri=seeds.get_fav_songs_uri(user=user_id)
        track_names, track_artist=get_song_info(song_uris=song_uri)
        return song_uri, track_names, track_artist
    @staticmethod
    def get_stored_seeds(user_ID:str ):
        session=ScopedSession()
        try:
            recs=session.query(Liked).filter(Liked.user_id==user_ID).all()
            seed_IDs=[]
            for rec in recs:
                if(rec.track_id not in seed_IDs):
                    seed_IDs.append(rec.track_id)
            return seed_IDs
        finally:
            session.close()
    @staticmethod
    def latest_record_date(user_ID:str):
        #returns the last time a record was pushed for this user 
        
        session=ScopedSession()
        try: 
            recs= session.query(Liked).filter(Liked.track_id==user_ID)
            earliest=recs[0].date_recorded
            for rec in recs:
                if rec.date_recorded> earliest:
                    earliest= rec.date_recorded
            return earliest
        finally:
            session.close()
    @staticmethod
    def push_seeds( track_IDs:list, user:str):
        session=ScopedSession()
        now= datetime.datetime.now(pytz.timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
        #the timestamp used for all the records we are going to push right now 
        try:
            db_recs_for_user=seeds.get_stored_seeds(user_ID=user)
            for track in track_IDs:
                if track not in db_recs_for_user:
                    session.add(seeds.seed_tracks(user_id=user, date_recorded=now, track_id=track))
            session.commit()       
        finally:
            session.close()