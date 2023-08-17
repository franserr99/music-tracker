from base import ScopedSession
from models.history import History
from models.library import Library
from models.features import Features
from user_queries import user_id_list,create_user
import pandas as pd

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
    song_uri=get_fav_songs_uri(user=user_id)
    track_names, track_artist=get_song_info(song_uris=song_uri)
    return song_uri, track_names, track_artist
@staticmethod
def get_song_info( song_uris:list):
    track_names=[]
    track_artists=[]
    try:
        session=ScopedSession()
        library=session.query(Library).all()
        for track in song_uris:
            for lib_track in library:
                if track== lib_track.uri:
                    track_names.append(lib_track.track_name)
                    track_artists.append(lib_track.track_artists)
        return track_names, track_artists
    finally:
        session.close()

@staticmethod
def add_song( track_uri:str, track_name:str, track_artist:str):
    try: 
        session = ScopedSession()
        session.add(Library(uri=track_uri, track_name=track_name, track_artists=track_artist) )
        session.commit()
    finally:
        session.close()
        print('an error occured within the add_song method')
@staticmethod
def add_songs(track_uris: list, track_names:list, track_artists:list, df:pd.DataFrame):
    #PART ONE: add to the track library 
    if not track_uris or len(track_uris)==0:
        return 
    session = ScopedSession()
    db_lib=get_song_uris()
    need_features=[]
    try:    
        for i, track in enumerate(track_uris):
            if track not in db_lib:
                need_features.append(track)
                session.add(Library(uri=track, track_name=track_names[i], track_artists=track_artists[i]))
        session.commit()        
    finally:
        session.close()
   
    try:
        for index, row in df.iterrow():
            session.add(Features(track_id= row.iloc[-1],danceability=row.iloc[0], energy=row.iloc[1],
                                        key=row.iloc[2] ,loudness=row.iloc[3],  mode=row.iloc[4],
                                        speechiness=row.iloc[5],acousticness=row.iloc[6],instrumentalness= row.iloc[7],
                                        liveness=row[8].iloc, valence=row.iloc[9],tempo=row.iloc[10]))
        session.commit()    
    finally:
        session.close()
@staticmethod
def get_song_uris():
    try:
        session = ScopedSession()
        song_URIs=[track_library.uri for track_library in session.query(Library).all() ]
        print(song_URIs)
        print(session.query(Library).all())
        #sys.exit(1)
        return song_URIs
    finally:
        session.close()
@staticmethod
def get_audio_features(tracks_uri:list):        
    #returns a 3 -tuple 
    # one of the three elements may be null (need to check that this is possible in pythoon )
    if len(tracks_uri)==0:
        return
    #get the audiofeatures for a specific song if we have it 
    session = ScopedSession()
    songs_features=[]
    try:
        for track in tracks_uri:
            feat=[]
            features=session.query(Features).filter(Features.track_id==track).first()
            feat.append(features.danceability)
            feat.append(features.energy)
            feat.append(features.key)
            feat.append(features.loudness)
            feat.append(features.mode)
            feat.append(features.speechiness)
            feat.append(features.acousticness)
            feat.append(features.instrumentalness)
            feat.append(features.liveness)
            feat.append(features.valence)
            feat.append(features.tempo)
            feat.append(track)
            songs_features.append(feat)
        return songs_features
    finally:
        session.close() 
@staticmethod
def song_in_db( track_uri:str): 
    db_songs= get_song_uris()
    if track_uri not in db_songs:
        return False
    else:
        return True
