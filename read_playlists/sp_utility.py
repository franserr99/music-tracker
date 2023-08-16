import spotipy, os, sys, json, requests
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

scope= "user-library-read user-read-playback-position user-top-read user-read-recently-played playlist-read-private"

def setup():
    load_dotenv("sp.env")         
    try: 
        #load_dotenv should load env var, now just check they exist in the enviorment
        os.environ["SPOTIPY_CLIENT_SECRET"] 
        os.environ['SPOTIPY_CLIENT_ID']
        os.environ["SPOTIPY_REDIRECT_URI"]
    except:
        print("one of these were not set as an enviormental variable, needed for successful execution")
        sys.exit(1) #use this instead of exit() bc it speaks to interpreter, not safe in prod env
def get_tracks(client:spotipy.Spotify, oauth:SpotifyOAuth,  user_playlistIDs:list, with_audio=True):
    user_tracks_IDX ,user_tracks_names, user_track_artists= extractInfo(client, oauth, user_playlistIDs)
    #changing to a df in here 
    user_df=pd.DataFrame({ 'id':user_tracks_IDX, 'track name': user_tracks_names, 'artist':user_track_artists})
    user_df.drop_duplicates(inplace=True)
    user_df.dropna()
    user_df.reset_index(drop=True, inplace=True)
    if(with_audio):
        user_df_with_features=get_audio_info(client,oauth, user_df)
        return user_df_with_features
    else:
        return  user_df
def extractInfo(client:spotipy.Spotify, oauth:SpotifyOAuth, playlistIDs:list): 
    all_tracks_IDX=[]
    all_track_names=[]
    all_track_artists=[]

    for id in playlistIDs:
        #keep track of counts to make sure it lines up later
        count_IDX= len(all_tracks_IDX)
        count_names=len(all_track_names)
        count_artists=(len(all_track_artists))
        #get first page of tracks
        tracks=client.playlist_tracks(id)
        tracks_IDX, tracks_name, artist_names=get_tracks_info(tracks)
        #add to our global lists
        all_tracks_IDX.extend(tracks_IDX)
        all_track_names.extend(tracks_name)
        all_track_artists.extend(artist_names)
        #go through remaining pages if any exist
        while(tracks['next']): 
            token=dict(oauth.get_cached_token())
            tracks=requests.get(tracks['next'], headers={"Authorization":  token['token_type']+" "+token['access_token']}).json()
            tracks_IDX, tracks_name, artist_names=get_tracks_info(tracks)
            all_tracks_IDX.extend(tracks_IDX)
            all_track_names.extend(tracks_name)
            all_track_artists.extend(artist_names)
        #count check
        count_IDX_after_playlist= len(all_tracks_IDX)
        count_names_after_playlist=len(all_track_names)
        count_artist_after_playlist= len(all_track_artists)
        assert (tracks['total']==(count_IDX_after_playlist-count_IDX)== (count_names_after_playlist-count_names )== (count_artist_after_playlist-count_artists))
    return all_tracks_IDX,all_track_names,all_track_artists
def get_tracks_info(tracks:dict):
    tracks_URI=[]
    tracks_name=[]
    artists_name=[]
    for item in tracks['items']:
        tracks_URI.append(item['track']['uri'])
        tracks_name.append(item['track']['name'])
        #get first artist associated with the song in the json obj
        artists_name.append(item['track']['artists'][0]['name']) 
    assert(len(tracks_URI)==len(tracks_name)==len(artists_name))
    return tracks_URI, tracks_name, artists_name
def get_audio_info( client:spotipy.Spotify, oauth:SpotifyOAuth, parent_df:pd.DataFrame):
    parent_df.reset_index(inplace=True, drop=True)
    partitioned_list=[]
    trackIDX=parent_df['id'][:]
    #prep data: break into 100 item chunks
    for i in range (0, len(trackIDX), 100): 
        partitioned_list.append(trackIDX[i:i+100])
    all_features=dict(client.audio_features(partitioned_list[0])[0])
    #get numerical data
    feature_column_names=list(all_features.keys())[:-7] 
    #keep a copy to make sure data lines up later
    feature_column_names.append('id') 
    songs_audio_features=[]
    #account for songs that dont have audio features
    all_bad_indices=[]
    #iterate in chunks
    for k, chunk in enumerate(partitioned_list):
        features=list(client.audio_features(chunk)) 
        assert(len(features)==len(chunk))
        #clean up data
        if None in features:  
            bad_indices=[]
            #get indicies of null values
            for i, v in enumerate(features): 
                if(v is None):
                    #account for the partioning 
                    all_bad_indices.append(int(i+((k)*100)))
                    bad_indices.append(i) 
            #get rid of items in feature list that are null
            for j in range (len(bad_indices)): 
                features.pop(bad_indices[j])    
        #removed all nulls by now, dealing with only a list of dictionaries
        for song_features in features: 
            feats=[]
            for column_name in feature_column_names:
                feats.append(song_features[column_name])
            songs_audio_features.append(feats)
    eligible_parents=parent_df.drop(index=all_bad_indices)
    eligible_parents.dropna(inplace=True)
    eligible_parents.reset_index(inplace=True, drop=True)
    assert(len(eligible_parents['id'][:])== len(songs_audio_features)), "the tracks were not dropped correctly somewhere"
    features_df=pd.DataFrame(songs_audio_features,columns=feature_column_names)
    features_df.dropna(inplace=True)
    features_df.reset_index(drop=True, inplace=True)
    complete_df=pd.concat([eligible_parents,features_df], axis=1)
    complete_df.reset_index(inplace=True, drop=True)
    return complete_df      
