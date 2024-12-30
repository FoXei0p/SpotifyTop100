import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from dotenv import load_dotenv
load_dotenv()
CLINT_ID = os.getenv("CLIENT_ID")
CLINT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URI")

# Public API
public_response = spotipy.client.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLINT_ID,
                                                                       client_secret=CLINT_SECRET))
# private API
private_response = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLINT_ID,
                                                    client_secret=CLINT_SECRET,
                                                    redirect_uri=REDIRECT_URL,
                                                    scope="playlist-read-private playlist-modify-private"))
# User ID
USER_ID = private_response.me()['id']

# existing playlist
existing_playlist = []
playlists = private_response.user_playlists(user=USER_ID)
for playlist in playlists["items"]:
    existing_playlist.append(playlist["name"].lower())

# new playlist Generator
playlist_name = input("PlayList Name: ")
descr = input("Playlist description: ")
while True:
    try:
        if playlist_name.lower() in existing_playlist:
            raise ValueError("Name with this Playlist already Exist please enter different One")
        new_playlist_mkr = private_response.user_playlist_create(user=USER_ID, name=playlist_name, public=False,
                                                                 description=descr)
        print(f"Playlist created: {new_playlist_mkr['name']} with ID: {new_playlist_mkr['id']}")
        break
    except ValueError as e:
        print(e)
        playlist_name = input("Enter a new Playlist Name: ")











