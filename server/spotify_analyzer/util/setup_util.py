import os
import sys

from dotenv import load_dotenv


scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def setup():
    if (os.getenv("SPOTIPY_CLIENT_SECRET") and
        os.getenv("SPOTIPY_CLIENT_ID") and
            os.getenv("SPOTIPY_REDIRECT_URI")):
        return
    load_dotenv("sp.env")
    try:
        # load_dotenv should load env var,
        # now just check they exist in the enviorment
        os.environ["SPOTIPY_CLIENT_SECRET"]
        os.environ['SPOTIPY_CLIENT_ID']
        os.environ["SPOTIPY_REDIRECT_URI"]
    except Exception:
        print("one of these were not set as an enviormental variable")
        # use this instead of exit() bc it speaks to interpreter
        sys.exit(1)
