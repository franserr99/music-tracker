from . import history_blueprint

from db.queries.history_queries import get_listening_history
from db.queries.history_queries import get_listening_history_by_term
from db.queries.history_queries import get_most_recent_history
from db.queries.history_queries import get_songs_heard
from db.queries.history_queries import push_history_data

@history_blueprint.route('/get_listening_history')
def listening_history(user):
    return get_listening_history(user_id=user)
@history_blueprint.route('/get_listening_history_by_term')
def listening_history_by_term(user,term):
    return get_listening_history_by_term(user_id=user,term=term)
@history_blueprint.route('/get_most_recent_history')
def most_recent_history():
    return get_most_recent_history()
@history_blueprint.route('/get_songs_heard')
def songs_heard():
    return get_songs_heard()
@history_blueprint.route('/push_history_data')
def add_history(records,term,id):
    push_history_data(records,term,id)
    return