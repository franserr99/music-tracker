from . import feature_blueprint
from typing import List
from db.queries.features_queries import get_audio_features
@feature_blueprint.route('/features')
def get_features(songs:List(str)):
    return get_audio_features(tracks_uri=songs)
    