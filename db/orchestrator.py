from api.top_tracks.user_top_tracks import monthly_tracks
from db.queries.library_queries import add_songs
def main():
    tracks=monthly_tracks()
    print("done")
    add_songs(df=tracks)

    pass
if __name__=='__main__':
    main()
