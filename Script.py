import os
import requests
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import urllib.parse

SPOTIFY_CLIENT_ID = input("Spotify Client ID: ")
SPOTIFY_CLIENT_SECRET = input("Spotify Client Secret: ")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-library-read"
))


def sanitize_filename(name):
    return "".join(c for c in name if c not in r'<>:"/\|?*').strip()

def search_maps(search_query):
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://api.beatsaver.com/search/text/0?q={encoded_query}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error from the BeatSaverAPI (Status {response.status_code}).")
        return []
    data = response.json()
    return data.get('docs', [])

def download_map(map_id, filename, save_path):
    download_url = f"https://beatsaver.com/api/download/{map_id}"
    save_file = os.path.join(save_path, filename)

    if os.path.exists(save_file):
        print(f"✅ Already existing: {filename}")
        return

    with requests.get(download_url, stream=True) as r:
        total_size = int(r.headers.get('content-length', 0))
        with open(save_file, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                size = f.write(chunk)
                bar.update(size)
    print(f"✅ Saved: {save_file}")

def search_and_download(song_name, artist_name, save_path):
    search_query = f"{artist_name} - {song_name}"
    print(f"\n🔎 Searching maps for: {search_query}")

    maps = search_maps(search_query)
    if not maps:
        print("⚠️ No map has been found!")
        return

    selected_map = maps[0]
    map_id = selected_map['id']

    filename = sanitize_filename(f"{artist_name} - {song_name}.zip")
    download_map(map_id, filename, save_path)


save_path = input("File path where it should be saved (custom maps path of your game): ")
if not os.path.exists(save_path):
    os.makedirs(save_path)

print("\n🚀 Getting your favourite songs from spotify...\n")

offset = 0
limit = 50

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    items = results['items']

    if not items:
        break

    for item in items:
        track = item['track']
        song_name = track['name']
        artist_name = track['artists'][0]['name']
        print(f"\n🎵 {artist_name} - {song_name}")
        search_and_download(song_name, artist_name, save_path)
        time.sleep(1)

    offset += limit

print("\n🎉 Done every song was saved!")
