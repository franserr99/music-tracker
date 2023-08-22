from . import history_blueprint

from db.queries.history_queries import get_listening_history
from db.queries.history_queries import get_listening_history_by_term
from db.queries.history_queries import get_most_recent_history
from db.queries.history_queries import get_songs_heard
from db.queries.history_queries import push_history_data

@history_blueprint.route('/features')
def listening_history():
    pass
@history_blueprint.route('/features')
def listening_history_by_term():
    pass

@history_blueprint.route('/features')
def most_recent_history():
    pass

@history_blueprint.route('/features')
def songs_heard():
    pass

@history_blueprint.route('/features')
def add_history():
    pass
    
    