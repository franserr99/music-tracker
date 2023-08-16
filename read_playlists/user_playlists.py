import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import sp_utility
def main(both=True, user=True):
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
            return user_tracks
def begin_build(client:spotipy.Spotify, oauth:SpotifyOAuth, user_flag:bool, with_audio=True):
    playlists_IDX=[]
    playlists=client.current_user_playlists()
    for playlist in playlists['items']:
        if(user_flag):
            if playlist['owner']['id'] ==client.me()['id']:
                playlists_IDX.append(playlist['id'])
        else:
            if playlist['owner']['id'] !=client.me()['id']:
                playlists_IDX.append(playlist['id'])

    df_with_audio=sp_utility.get_tracks(client, oauth, playlists_IDX,True)
    return df_with_audio
if __name__ == "__main__":
    main()