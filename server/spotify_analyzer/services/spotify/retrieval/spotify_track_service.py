from .. import sp_utility
import spotipy
from ..spotify_token_handler import SpotifyTokenHandler


class SpotifyTrackService:
    def __init__(self, client: spotipy.Spotify,
                 token_handler: SpotifyTokenHandler):
        self.client = client
        self.token_handler = token_handler

    # main method #1
    def get_monthly_tracks(self, term="short_term"):
        this_month_tracks = self.begin_build(term=term, type='tracks')
        print(this_month_tracks.columns)
        print(this_month_tracks)
        return this_month_tracks

    # main method #2    
    def get_monthly_artists(self, term="short_term"):
        this_month_artists = self.begin_build(term=term, type='artists')
        print(this_month_artists)
        return this_month_artists

    # common entry point for both main methods
    def begin_build(self, term, type):
        try:
            # Your Spotify API call logic
            if (type == 'tracks'):
                dict = self.client.current_user_top_tracks(
                    20, offset=0, time_range=term)
                df_with_audio = sp_utility.get_tracks(
                    client=self.client, token_handler=self.token_handler,
                    source=("t", dict), with_audio=True)
                return df_with_audio
            elif (type == 'artists'):
                dict = self.client.current_user_top_artists(
                    20, offset=0, time_range=term)
                print(dict)
                artists = []
                for item in dict['items']:
                    artist = {'name': item['name'], 'genres': item['genres'],
                              'uri': item['uri'], 'images': item['images'],
                               }
                    artists.append(artist)
                    
                return artists

        except Exception as e:
            print("********")
            print(e.response.text)
            # This will print more details about the error
            raise e
 
    # logic to filter through and pick the top artists
    def top_n_artists(self, tracks_artists):
        # filter the songs by artists
        artist_dict = {}
        for k, track_artists in enumerate(tracks_artists):
            artists = track_artists.split(",")
            for creator in artists:
                cre = str(creator.strip())
                # the list as a value for the key:
                # value pairing does not exist yet
                if cre not in artist_dict:
                    artist_dict[cre] = []
                artist_dict[cre].append(k)
        # every artist has a list associated with the songs they are in
        all_artists = artist_dict.keys()
        if len(artist_dict) <= 5:
            # all artists are already your top artists
            top_artists = all_artists
        else:
            top_artists = []
            for creator in artist_dict.keys():
                top_artists.append(creator)
                if len(top_artists) == 6:
                    break
        # top artist by how many of their songs are in the api results
        for artist in all_artists:
            appearances = len(artist_dict[artist])
            # replace the first time with a bigger fish
            for k, top_artist in enumerate(top_artists):
                if appearances > len(artist_dict[top_artist]):
                    top_artists[k] = artist
                    break
        return top_artists
    # paginate and process all of the responses

    def unique_tracks_all_terms(self):
        # id, name, artist: structure of the tuple returned
        # init the iterables w/ short-term
        short_term = self.begin_build("short_term")
        medium_term = self.begin_build("medium_term")
        long_term = self.begin_build("long_term")
        # set up var
        track_idx = short_term[0][:]
        track_names = short_term[1][:]
        track_artists = short_term[2][:]
        unique_tuple = (track_idx, track_names, track_artists)
        # get unique items from medium and then long term
        self.addUniqueItems(unique_tuple=unique_tuple, term=medium_term)
        self.addUniqueItems(unique_tuple=unique_tuple, term=long_term)
        # check
        assert (len(track_idx) == len(track_artists) == len(track_names))
        return track_idx, track_names, track_artists

    def addUniqueItems(self, unique_tuple, term):
        track_idx = unique_tuple[0]
        track_names = unique_tuple[1]
        track_artists = unique_tuple[2]

        for i, track in enumerate(term[0]):
            if track not in track_idx:
                track_idx.append(track)
                track_artists.append(term[2][i])
                track_names.append(term[1][i])

