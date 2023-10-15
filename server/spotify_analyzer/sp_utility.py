import spotipy, os, sys,requests
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

scope= "user-library-read user-read-playback-position user-top-read user-read-recently-played playlist-read-private"
#TODO
#def welcome_user(engine: sqlalchemy.engine.Engine, client:spotipy.Spotify): 
#    spotipy_id=client.me()['id']
#    db_sp_id=db_util.user_util.user_id_list(engine=engine)
#    if spotipy_id not in db_sp_id: 
#        db_util.user_util.create_user(spotipy_id, engine)
def setup():
    if(os.getenv("SPOTIPY_CLIENT_SECRET") and os.getenv("SPOTIPY_CLIENT_ID") and os.getenv("SPOTIPY_REDIRECT_URI")):
        return
    load_dotenv("sp.env")         
    try: 
        #load_dotenv should load env var, now just check they exist in the enviorment
        os.environ["SPOTIPY_CLIENT_SECRET"] 
        os.environ['SPOTIPY_CLIENT_ID']
        os.environ["SPOTIPY_REDIRECT_URI"]
    except:
        print("one of these were not set as an enviormental variable, needed for successful execution")
        sys.exit(1) #use this instead of exit() bc it speaks to interpreter, not safe in prod env
def get_tracks(client:spotipy.Spotify, oauth:SpotifyOAuth,  source=None, with_audio=True):
    
    user_tracks_IDX ,user_tracks_names, user_track_artists= process_source(client, oauth, source)
    

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
def paginate_results(tracks:dict, idx:list, track_names:list, artist_names:list, oauth,choice):

    token=dict(oauth.get_cached_token())
    type=token['token_type']
    access_token=token['access_token']

    while(tracks['next']):
        tracks= requests.get(tracks['next'], headers={ 'Authorization': type+" "+access_token }).json()
        if(choice=="t"):
            more_idx, more_track_names,more_artist_names= get_tracks_info(tracks,"t")
        elif(choice=="p"):
            more_idx, more_track_names,more_artist_names= get_tracks_info(tracks,"p")
        idx.extend(more_idx)
        track_names.extend(more_track_names)
        artist_names.extend(more_artist_names)
def process_source(client:spotipy.Spotify, oauth:SpotifyOAuth, source): 
    track_idx=[]
    track_name=[]
    track_artist=[]

    if(source[0]=="p"):
        for id in source[1]:
            #keep track of counts to make sure it lines up later
            count_IDX= len(track_idx)
            count_names=len(track_name)
            count_artists=(len(track_artist))
            #get first page of tracks
            tracks=client.playlist_tracks(id)
            t_idx, t_name, a_name=get_tracks_info(tracks,"p")
            #add to our global lists
            track_idx.extend(t_idx)
            track_name.extend(t_name)
            track_artist.extend(a_name)
            #page if needed
            paginate_results(tracks=tracks,idx=track_idx,track_names=track_name,artist_names=track_artist,oauth=oauth,choice="p")
            #count check
            count_IDX_after_playlist= len(track_idx)
            count_names_after_playlist=len(track_name)
            count_artist_after_playlist= len(track_artist)
            assert (tracks['total']==(count_IDX_after_playlist-count_IDX)== (count_names_after_playlist-count_names )== (count_artist_after_playlist-count_artists))
    elif(source[0]=="t"):
        tracks=get_tracks_info(source[1],"t")
        #add to our global lists
        track_idx.extend(tracks[0])
        track_name.extend(tracks[1])
        track_artist.extend(tracks[2])
        if(source[1]['next']): 
            paginate_results(source[1], track_idx, track_name, track_artist,oauth=oauth,choice="t")
    return track_idx,track_name,track_artist
def get_tracks_info(tracks:dict,choice):
    tracks_URI=[]
    tracks_name=[]
    artists_name=[]
    for item in tracks['items']:
        if(choice=="p"):
            tracks_URI.append(item['track']['uri'])
            tracks_name.append(item['track']['name'])
            #get first artist associated with the song in the json obj
            artists_name.append(item['track']['artists'][0]['name']) 
        elif(choice=="t"):
            #different json structure
            #this is for top monthly tracks
            tracks_URI.append(item['uri'])
            tracks_name.append(item['name'])
            artists_name.append(item['artists'][0]['name']) 
    assert(len(tracks_URI)==len(tracks_name)==len(artists_name))
    return tracks_URI, tracks_name, artists_name
        
def get_audio_info( client:spotipy.Spotify, oauth:SpotifyOAuth, parent_df:pd.DataFrame):
    print(parent_df)
    parent_df.reset_index(inplace=True, drop=True)
    partitioned_list=[]
    trackIDX=parent_df['id'][:]
    #prep data: break into 100 item chunks
    for i in range (0, len(trackIDX), 100): 
        partitioned_list.append(trackIDX[i:i+100])
    all_features=dict(client.audio_features(partitioned_list[0])[0])
    #print(all_features.keys())
    #get numerical data
    feature_column_names=list(all_features.keys())[:-7] 
    #keep a copy to make sure data lines up later
    #feature_column_names.append('id') 
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
