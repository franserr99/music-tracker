from typing import List
from ..service_dtos import TrackData
class SpotifyDataExtractor:

    @staticmethod
    def get_track_dto():
        pass

    @staticmethod
    def get_list_of_track_dtos():
        pass

    @staticmethod
    def get_album_dto():
        pass

    @staticmethod
    def get_list_of_album_dtos():
        pass

    @staticmethod
    def get_artist_dto():
        pass

    @staticmethod
    def get_list_of_artist_dtos():
        pass

    @staticmethod
    def get_playlist_dto():
        pass

    @staticmethod
    def get_list_of_playlist_dtos():
        pass

    # these are the functions called at a high level
    # will refactor where possible to reduce code duplicates
    # might be able to put them all into a single method
    # but without flags for conditional calling
    @staticmethod
    def parseTopTracksResponse(records):
        # needs to return a tuple, i dont want to refactor my other
        # code and this is the simplest option
        # first element is the dict with the array of dtos for each entity
        # second one will be for my foreign key relationships
        # need to return an album dict, keys are album uri and value is array
        # in the caller, if there is no corresponding array or it is empty,
        # then dont need to add the relationship-- singles can be a track
        #   (dont create album for it)
        pass

    @staticmethod
    def parseTopArtistsResponse():
        pass

    @staticmethod
    def parsePlaylistResponse():
        pass

    @staticmethod 
    def get_list_of_track_uris(tracks: List[TrackData]):
        track_uris = []
        for track in tracks:
            track_uris.append(track['uri'])
        return track_uris

