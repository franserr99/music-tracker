from . import liked_blueprint
from db.queries.liked_queries import recs
from db.queries.liked_queries import seeds
#recs:
    #get_potential_recs
    #latest_record_date
    #push_pontential_recs
@liked_blueprint.route('/get_potential_recs')
def get_potential_recs(user):
    return recs.get_potential_recs(user_ID=user)
#TODO:need to fix this and have the actual implementation
@liked_blueprint.route('/latest_record_date')
def latest_record_date():
    return recs.latest_record_date()
@liked_blueprint.route('/push_pontential_recs')
def push_pontential_recs(track_idx,user):
    recs.push_pontential_recs(track_IDs=track_idx,user=user)
#seed
    #get_fav_songs_uri
    #fav_songs_info
    #get_stored_seeds
    #latest_record_date
    #push_seeds
@liked_blueprint.route('/get_fav_songs_uri')
def get_fav_songs_uri(user):
    return seeds.get_fav_songs_uri(user=user)
@liked_blueprint.route('/fav_songs_info')
def fav_songs_info(user):
    return seeds.fav_songs_info(user_id=user)
@liked_blueprint.route('/get_stored_seeds')
def get_stored_seeds(user):
    return seeds.get_stored_seeds(user_ID=user)
@liked_blueprint.route('/push_seeds')
def push_seeds(track_idx,user):
    seeds.push_seeds(track_IDs=track_idx,user=user)