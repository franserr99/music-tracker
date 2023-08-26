from . import library_blueprint
from db.queries.library_queries import get_listened_artists
from db.queries.library_queries import get_song_info
from db.queries.library_queries import get_song_uris
from db.queries.library_queries import add_song
from db.queries.library_queries import add_songs
from db.queries.library_queries import song_in_db
from db.queries.library_queries import songs_not_in_db
from typing import List
import pandas as pd

@library_blueprint.route('/listned_artists')
def listned_artists(user):
    return get_listened_artists(user_id=user)

@library_blueprint.route('/song_info')
def song_info(songs:List(str)):
    return get_song_info(songs)

@library_blueprint.route('/all_songs')
def all_songs():
    return get_song_uris()

@library_blueprint.route('/push_song')
def push_song(id,name,artist):
    add_song(id,name,artist)

@library_blueprint.route('/push_songs')
def push_songs(songs:pd.DataFrame):
    #need some kind of df
    add_songs(songs)

@library_blueprint.route('/is_song_in')
def is_song_in_db(track_id):
    return song_in_db(track_uri=track_id)

@library_blueprint.route('/songs_not_in_db')
def tracks_not_in_db(track_idx):
    return songs_not_in_db(track_idx)

