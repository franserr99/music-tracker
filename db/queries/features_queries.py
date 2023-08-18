from db.base import ScopedSession
from db.models.features import Features

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