from db.base import ScopedSession
from db.models.history import History
from db.models.library import Library
from db.models.features import Features
import pandas as pd
from db.queries.consts import DANCEABILITY,ENERGY,KEY,LOUDNESS,MODE,SPEECHINESS,ACOUSTICNESS,INSTRUMENTALNESS,LIVENESS,VALENCE,TEMPO



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


def add_song( track_uri:str, track_name:str, track_artist:str):
    try: 
        session = ScopedSession()
        session.add(Library(uri=track_uri, track_name=track_name, track_artists=track_artist) )
        session.commit()
    finally:
        session.close()
        print('an error occured within the add_song method')

#TODO: figure out how you want this implementation 

def add_songs(df:pd.DataFrame):
    print("adding tracks...")
    track_idx=df.iloc[0,:].to_list()
    track_names=df.iloc[1,:].to_list()
    track_artists=df.iloc[2,:].to_list()
    #PART ONE: add to the track library 
    if not track_idx or len(track_idx)==0:
        print("no tracks to add")
        return 
    session = ScopedSession()
    db_lib=get_song_uris()
    need_features=[]
    try:    
        for i, track in enumerate(track_idx):
            if track not in db_lib:
                need_features.append(track)
                session.add(Library(uri=track, track_name=track_names[i], track_artists=track_artists[i]))
                session.add(Features(track_id= track,danceability=df.iloc[i,DANCEABILITY], energy=df.iloc[i,ENERGY],
                                        key=df.iloc[i,KEY] ,loudness=df.iloc[i,LOUDNESS],  mode=df.iloc[i,MODE],
                                        speechiness=df.iloc[i,SPEECHINESS],acousticness=df.iloc[i,ACOUSTICNESS],instrumentalness= df.iloc[i,INSTRUMENTALNESS],
                                        liveness=df.iloc[i,LIVENESS], valence=df.iloc[i,VALENCE],tempo=df.iloc[i,TEMPO]))
        session.commit()        
    finally:
        session.close()

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


def song_in_db( track_uri:str): 
    db_songs= get_song_uris()
    if track_uri not in db_songs:
        return False
    else:
        return True

def get_listened_artists(user_id:str ): 
    all_artists=[]
    song_names, song_artists= get_song_info()
    for song_artist in song_artists:
        artists=song_artist.split(",")
        for creator in artists:
            cre=str(creator.strip())
            if cre not in all_artists: #the list as a value for the key:value pairing does not exist yet
                all_artists.append(cre)
    return all_artists

def songs_not_in_db(track_idx):
    not_in_db=[]
    db_songs=get_song_uris()

    for track in track_idx:
        if(track not in db_songs):
            not_in_db.append(track)
    return not_in_db
