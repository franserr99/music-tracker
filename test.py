#assert that each file that deals with audio characteristics actually is matching up.
# might be something wrong when you pull the data and pop off the dataframe when no audio shows up
import read_playlists.user_playlists as user_playlists
import pandas as pd
import read_playlists.sp_utility as sp_utility
from spotipy.oauth2 import SpotifyOAuth
import random,spotipy

def main():
    user_df= user_playlists.main(False)
    sp_utility.setup()
    oauth=SpotifyOAuth(scope=sp_utility.scope)
    sp=spotipy.Spotify(auth_manager=oauth)
    verify(user_df, sp)
    print("could be verified!")

def verify(df:pd.DataFrame,client:spotipy.Spotify):
    n_randomChecks=10
    #check there are atleast more than 10 
    if(len(df)<10):
        n_randomChecks=len(df)
    n_items=len(df)
    for i in range (n_randomChecks):
        random_index=random.randint(0,n_items-1)
        checkAudio(df.loc[i,'id'],client,df.iloc[i:i+1,3:])
        pass
def checkAudio(idx,client:spotipy.Spotify, numerical_df:pd.DataFrame):
    features=list(client.audio_features(idx)) 
    columns=numerical_df.columns.to_list()
    for column in columns:
        assert features[column]==numerical_df[column]
if __name__ == "__main__":
    main()