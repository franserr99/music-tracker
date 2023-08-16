import spotipy, os, sys, json, requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from ratelimit import limits, sleep_and_retry
import time
from sklearn.metrics.pairwise import linear_kernel
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

def main():

    load_dotenv("sp.env")     
    scope= "user-library-read user-read-playback-position user-top-read user-read-recently-played playlist-read-private"
    
    try: 
        #load_dotenv should load env var, now just check they exist in the enviorment
        os.environ["SPOTIPY_CLIENT_SECRET"] 
        os.environ['SPOTIPY_CLIENT_ID']
        os.environ["SPOTIPY_REDIRECT_URI"]
    except:
        print("one of these were not set as an enviormental variable, needed for successful execution")
        sys.exit(1) #use this instead of exit() bc it speaks to interpreter, not safe in prod env
    
    #print(os.environ) debugging purposes 
    oauth=SpotifyOAuth(scope=scope)
    sp=spotipy.Spotify(auth_manager=oauth)
    
    print(" playlist maker where library is used to find playlists, potential reccomendedations are pulled from the playlists in library that user hasnt created")
    begin_build(sp, oauth)

def begin_build(client:spotipy.Spotify, oauth:SpotifyOAuth):
    print( "begin_build method")

    potential_seed_playlists_IDX=[]
    user_created_playlists_IDX=[]
    playlists=client.current_user_playlists()

    for playlist in playlists['items']:
        if playlist['owner']['id'] !=client.me()['id']:
            print("playlist with ID"+ playlist['owner']['id']+" is going into the potential seed tracks")
            potential_seed_playlists_IDX.append(playlist['id'])            
        else: 
            user_created_playlists_IDX.append(playlist['id'])
    #make an assert statement for the added length of both the lists to the total we got from the json 
    seed_df,user_df=get_tracks(client, oauth, potential_seed_playlists_IDX, user_created_playlists_IDX)
    
def get_tracks(client:spotipy.Spotify, oauth:SpotifyOAuth, seed_playlistIDs:list, user_playlistIDs:list):
    print("-------------------------------start of get_tracks method----------------------------")

    seed_tracks_IDX, seed_track_names, seed_track_artists=extractInfo(client, oauth, seed_playlistIDs)
    user_tracks_IDX ,user_tracks_names, user_track_artists= extractInfo(client, oauth, user_playlistIDs)
    #changing to a df in here 
    seed_df=pd.DataFrame({ 'id':seed_tracks_IDX, 'track name': seed_track_names, 'artist':seed_track_artists})
    user_df=pd.DataFrame({ 'id':user_tracks_IDX, 'track name': user_tracks_names, 'artist':user_track_artists})
    seed_df.drop_duplicates(inplace=True)
    seed_df.dropna()
    seed_df.reset_index(drop=True, inplace=True)
    user_df.drop_duplicates(inplace=True)
    user_df.dropna()
    user_df.reset_index(drop=True, inplace=True)

    seed_trackIDX= seed_df['id']
    user_trackIDX=user_df['id']

    seed_df_with_features=get_audio_info(client,oauth, seed_df)
    user_df_with_features=get_audio_info(client,oauth, user_df)

    print(seed_df)
    print(user_df)
    seed_df_with_features.to_csv('seedwithfeatures.csv')
    user_df_with_features.to_csv('userwithfeatures.csv')
    return seed_df, user_df
def extractInfo(client:spotipy.Spotify, oauth:SpotifyOAuth, playlistIDs:list): 
    
    all_tracks_IDX=[]
    all_track_names=[]
    all_track_artists=[]

    for id in playlistIDs:
        count_IDX= len(all_tracks_IDX)
        count_names=len(all_track_names)
        count_artists=(len(all_track_artists))
        
        tracks=client.playlist_tracks(id)
        tracks_IDX, tracks_name, artist_names=get_tracks_info(tracks)
        all_tracks_IDX.extend(tracks_IDX)
        all_track_names.extend(tracks_name)
        all_track_artists.extend(artist_names)

        while(tracks['next']): #go through remaining pages if any exist
            token=dict(oauth.get_cached_token())
            tracks=requests.get(tracks['next'], headers={"Authorization":  token['token_type']+" "+token['access_token']}).json()
            tracks_IDX, tracks_name, artist_names=get_tracks_info(tracks)
            all_tracks_IDX.extend(tracks_IDX)
            all_track_names.extend(tracks_name)
            all_track_artists.extend(artist_names)
        
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
        artists_name.append(item['track']['artists'][0]['name']) #get first artist associated with the song in the json obj
    assert(len(tracks_URI)==len(tracks_name)==len(artists_name))
    return tracks_URI, tracks_name, artists_name
def get_audio_info( client:spotipy.Spotify, oauth:SpotifyOAuth, parent_df:pd.DataFrame):
    parent_df.reset_index(inplace=True, drop=True)

    partitioned_list=[]
    trackIDX=parent_df['id'][:]

    for i in range (0, len(trackIDX), 100): #prep data: break into 100 item chunks
        partitioned_list.append(trackIDX[i:i+100])
    
    all_features=dict(client.audio_features(partitioned_list[0])[0])
    feature_column_names=list(all_features.keys())[:-7] #get numerical data
    feature_column_names.append('id') #keep a copy to make sure data lines up later

    songs_audio_features=[]
    #account for songs that dont have audio features
    all_bad_indices=[]

    for k, chunk in enumerate(partitioned_list):
        features=list(client.audio_features(chunk)) 
        print(features)
        print(len(chunk))
        #sys.exit(1)
        assert(len(features)==len(chunk))
        if None in features: #clean up data 
            print(features)
            bad_indices=[]
            for i, v in enumerate(features): #get indicies of null values
                if(v is None):
                    print(i)
                    all_bad_indices.append(int(i+((k)*100))) #account for the partioning 
                    bad_indices.append(i) 
            for j in range (len(bad_indices)): #get rid of items in feature list that are null
                features.pop(bad_indices[j])    
        for song_features in features: #removed all nulls by now, dealing with only a list of dictionaries
            feats=[]
            for column_name in feature_column_names:
                feats.append(song_features[column_name])
            print (feats)
            sys.exit(1)
            songs_audio_features.append(feats)

    print(all_bad_indices)
  
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

main() 