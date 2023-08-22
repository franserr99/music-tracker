from . import library_blueprint
from db.queries.library_queries import get_listened_artists
from db.queries.library_queries import get_song_info
from db.queries.library_queries import get_song_uris
from db.queries.library_queries import add_song
from db.queries.library_queries import add_songs
from db.queries.library_queries import song_in_db
from db.queries.library_queries import songs_not_in_db




@library_blueprint.route('/listned_artists')
def listned_artists():
    pass
@library_blueprint.route('/song_info')
def song_info():
    pass
@library_blueprint.route('/all_songs')
def all_songs():
    pass
@library_blueprint.route('/push_song')
def push_song():
    pass
@library_blueprint.route('/push_songs')
def push_songs():
    pass
@library_blueprint.route('/is_song_in')
def is_song_in_db():
    pass
@library_blueprint.route('/are_songs_in_db')
def are_songs_in_db():
    pass

