import os
import spotipy
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUR_CLIENT_SECRET")
REDIRECT_URL = os.getenv("YOUR_REDIRECT_URI")

# Public API----------------------------------------------------------------------------------------------------
public_response = spotipy.client.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                                               client_secret=CLIENT_SECRET))
# private API----------------------------------------------------------------------------------------------------
private_response = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                             client_secret=CLIENT_SECRET,
                                                             redirect_uri=REDIRECT_URL,
                                                             scope="playlist-read-private playlist-modify-private"))
USER_ID = private_response.me()['id']

# user inputs---------------------------------------------------------------------------------------------
print("Top100 Songs Of Your Desired Time's\n")
playlist_name = input("PlayList Name: ")
descr = input("Playlist description: ")
date = input("Which year of top100 song you want to get? 'STRICTLY Enter in this format YYYY-MM-DD': ")
print("\n")

# top 100song from billboard scrapped------------------------------------------------------------------------

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
url_billboard = "https://www.billboard.com/charts/hot-100/" + date

response = requests.get(url=url_billboard, headers=header)
soup = BeautifulSoup(response.text, 'html.parser')
selector = soup.select("li ul li h3")
song_name = [song.get_text().strip() for song in selector]


# get songs URI from Spotify--------------------------------------------------------------------------
track_uris = []
index = 0
year = date.split("-")[0]
print(f"Top100 songs from {date}-------------------------------")
for song in song_name:
    index += 1
    result = public_response.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result['tracks']['items'][0]['uri']
        print(index, song)
        track_uris.append(uri)
    except IndexError:
        print(f"{index, song} doesn't exist in Spotify. Skipped.")

# existing playlist---------------------------------------------------------------------------------
existing_playlist = []
playlists = private_response.user_playlists(user=USER_ID)
for playlist in playlists["items"]:
    existing_playlist.append(playlist["name"].lower())

# new playlist Generator-----------------------------------------------------------------------------------------
while True:
    try:
        if playlist_name.lower() in existing_playlist:
            raise ValueError("Name with this Playlist already Exist please enter different One\n")
        new_playlist_mkr = private_response.user_playlist_create(user=USER_ID, name=playlist_name, public=False,
                                                                 description=descr)
        print(f"Playlist created: {new_playlist_mkr['name']} with Playlist ID: {new_playlist_mkr['id']}")
        break
    except ValueError as e:
        print(e)
        playlist_name = input("Enter a new Playlist Name: ")

# added all the songs to playlist-------------------------------------------------------------------------------
playlist_id = new_playlist_mkr['id']
playlists = private_response.playlist_add_items( playlist_id=playlist_id,items=track_uris)


