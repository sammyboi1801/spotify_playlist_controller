from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
import os
from dotenv import load_dotenv, dotenv_values


load_dotenv()

scope_modify = "playlist-modify-public"

auth_manager = SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"), scope=scope_modify, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

current_playlist_name = f"{sp.playlist(os.getenv('PLAYLIST_ID'))['name']}"

def home(request):
    request.session.modified = True
    message = ""

    current_playlist_name = f"{sp.playlist(os.getenv('PLAYLIST_ID'))['name']}"
    if request.method == 'POST':
        if 'updated_playlist_name' in request.POST:
            update_name =request.POST['updated_playlist_name']
            password = request.POST['password']

            if password==os.getenv("PASSWORD") and update_name is not None:
                sp.playlist_change_details(playlist_id=os.getenv("PLAYLIST_ID"), name=update_name)
                message = "Playlist name updated!"
                current_playlist_name = f"{sp.playlist(os.getenv('PLAYLIST_ID'))['name']}"
            else:
                message = "Wrong password!"
    update_name = ""
    password = ""
    return render(request,"home.html",{"current_playlist_name":current_playlist_name,"message":message})