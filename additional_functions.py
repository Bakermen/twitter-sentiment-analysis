import spotipy
from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import os

load_dotenv()

token_id = os.getenv("client_id")
token_secret = os.getenv("client_secret")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=token_id, client_secret=token_secret))


def get_album_release_date(artist_name, album_name):
    try:
        artist = sp.search(q = 'artist:'+artist_name, type='artist')
        albums = sp.artist_albums(artist['artists']['items'][0]['id'])
        for i in albums['items']:
            if i['name'].lower() == album_name:
                release_date = i['release_date']
        date_obj = datetime.strptime(release_date, "%Y-%m-%d")
    except:
        return 0
    return date_obj


