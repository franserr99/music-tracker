from api.top_tracks.user_top_tracks import monthly_tracks
from db.queries import library_queries 
def main():
    tracks=monthly_tracks()
    print("done")
    library_queries.add_songs(df=tracks)

    pass
if __name__=='__main__':
    main()
