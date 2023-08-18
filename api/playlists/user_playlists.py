import spotipy,requests
from spotipy.oauth2 import SpotifyOAuth
from .. import sp_utility
def main(both=False, user=True):
    sp_utility.setup()
    oauth=SpotifyOAuth(scope=sp_utility.scope)
    sp=spotipy.Spotify(auth_manager=oauth)
    if(both):
        user_tracks=begin_build(sp, oauth,user_flag=True,with_audio=True)
        seed_tracks=begin_build(sp, oauth,user_flag=False,with_audio=True)
        return user_tracks,seed_tracks
    else:
        if(user):
            user_tracks=begin_build(sp, oauth,user_flag=True,with_audio=True)
            return user_tracks
        else:
            seed_tracks=begin_build(sp, oauth,user_flag=False,with_audio=True)
            return seed_tracks
def begin_build(client:spotipy.Spotify, oauth:SpotifyOAuth, user_flag:bool, with_audio=True):
    #do first page of playlists
    playlists_idx=[]
    playlists=client.current_user_playlists()
    process_page(playlists=playlists,user_flag=user_flag,client=client,playlist_idx=playlists_idx)
    #do more if needed
    if(playlists['next']):
        token=dict(oauth.get_cached_token())
        type=token['token_type']
        access_token=token['access_token']
        while playlists['next']:
            playlists= requests.get(playlists['next'], headers={ 'Authorization': type+" "+access_token }).json()
            process_page(playlists=playlists,user_flag=user_flag,client=client,playlist_idx=playlists_idx)

    df_with_audio=sp_utility.get_tracks(client, oauth, ("p",playlists_idx),True)
    return df_with_audio
def process_page(playlists,user_flag,client,playlist_idx):
    for playlist in playlists['items']:
        print(playlist)
        if(user_flag):
            print("playlist['owner']['id'] : ",playlist['owner']['id'] )
            print("client.me()['id']: ",client.me()['id'])
            if (playlist['owner']['id']==client.me()['id']):
                playlist_idx.append(playlist['id'])
        else:
            if (playlist['owner']['id'] !=client.me()['id']):
                playlist_idx.append(playlist['id'])
if __name__ == "__main__":
    main()