import spotipy
from spotipy.oauth2 import SpotifyOAuth
from api import sp_utility

def monthly_tracks():
    sp_utility.setup()
    oauth=SpotifyOAuth(scope=sp_utility.scope)
    sp=spotipy.Spotify(auth_manager=oauth)
    this_month_tracks=begin_build(client=sp,term="long_term",oauth=oauth)
    print(this_month_tracks)
    return this_month_tracks
#short_term, medium_term,long_term
def main(artistsOnly=True, term="short_term"): 
    this_month_tracks=monthly_tracks()
    print(this_month_tracks.columns)
    tracks_artists=this_month_tracks.iloc[:,2]
    top_artists=top_n_artists(tracks_artists=tracks_artists)
    print(top_artists)
#logic to filter through and pick the top artists
def top_n_artists(tracks_artists):
    #filter the songs by artists
    artist_dict={}
    for k ,track_artists in enumerate(tracks_artists):
        artists=track_artists.split(",")
        for creator in artists:
            cre=str(creator.strip())
            #the list as a value for the key:value pairing does not exist yet
            if cre not in artist_dict:
                artist_dict[cre]=[]
            artist_dict[cre].append(k)
    #every artist has a list associated with the songs they are in 
    all_artists=artist_dict.keys()
    if len(artist_dict)<=5:
        #all artists are already your top artists 
        top_artists=all_artists
    else :
        top_artists=[]
        for creator in artist_dict.keys():
            top_artists.append(creator)
            if len (top_artists)==6:
                break
    #top artist by how many of their songs are in the api results 
    for artist in all_artists:
        appearances=len(artist_dict[artist])
        #replace the first time with a bigger fish 
        for k ,top_artist in enumerate(top_artists):
            if appearances>len(artist_dict[top_artist]): 
                top_artists[k]=artist
                break
    return top_artists
#paginate and process all of the responses
def begin_build(term, client, oauth): 
    track_dict=client.current_user_top_tracks(20,offset=0,time_range= term )
    
    df_with_audio=sp_utility.get_tracks(client=client,oauth=oauth,source=("t",track_dict),with_audio=True)
    return df_with_audio

def unique_tracks_all_terms():
    #id, name, artist: structure of the tuple returned 
    #init the iterables w/ short-term
    short_term=begin_build("short_term")
    medium_term=begin_build("medium_term")
    long_term=begin_build("long_term")
    #set up var
    track_idx=short_term[0][:]
    track_names=short_term[1][:]
    track_artists=short_term[2][:]
    unique_tuple=(track_idx,track_names,track_artists)
    #get unique items from medium and then long term
    addUniqueItems(unique_tuple=unique_tuple,term=medium_term)
    addUniqueItems(unique_tuple=unique_tuple,term=long_term)
    #check
    assert(len(track_idx)==len(track_artists)==len(track_names))
    return track_idx,track_names,track_artists
def addUniqueItems(unique_tuple,term):
    track_idx=unique_tuple[0]
    track_names=unique_tuple[1]
    track_artists=unique_tuple[2]

    for i, track in enumerate(term[0]):
        if track not in track_idx:
            track_idx.append(track)
            track_artists.append(term[2][i])
            track_names.append(term[1][i])
if __name__=='__main__':
    main()
