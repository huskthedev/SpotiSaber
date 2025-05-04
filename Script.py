import os
import requests
from tqdm import tqdm
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import urllib.parse

# ==== Spotify Setup ====
SPOTIFY_CLIENT_ID = input("Spotify Client ID eingeben: ")
SPOTIFY_CLIENT_SECRET = input("Spotify Client Secret eingeben: ")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-library-read"
))

# ==== Hilfsfunktionen ====

def sanitize_filename(name):
    return "".join(c for c in name if c not in r'<>:"/\|?*').strip()

def search_maps(search_query):
    encoded_query = urllib.parse.quote(search_query)
    url = f"https://api.beatsaver.com/search/text/0?q={encoded_query}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Fehler bei der BeatSaver API (Status {response.status_code}).")
        return []
    data = response.json()
    return data.get('docs', [])

def download_map(map_id, filename, save_path):
    download_url = f"https://beatsaver.com/api/download/{map_id}"
    save_file = os.path.join(save_path, filename)

    if os.path.exists(save_file):
        print(f"✅ Bereits vorhanden: {filename}")
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
    print(f"✅ Gespeichert: {save_file}")

def search_and_download(song_name, artist_name, save_path):
    search_query = f"{artist_name} - {song_name}"
    print(f"\n🔎 Suche Beat Saber Maps für: {search_query}")

    maps = search_maps(search_query)
    if not maps:
        print("⚠️ Keine Maps gefunden!")
        return

    # Nimm die erste gefundene Map automatisch
    selected_map = maps[0]
    map_id = selected_map['id']

    filename = sanitize_filename(f"{artist_name} - {song_name}.zip")
    download_map(map_id, filename, save_path)

# ==== Hauptprogramm ====

save_path = input("Ordner-Pfad angeben, wo Songs gespeichert werden sollen: ")
if not os.path.exists(save_path):
    os.makedirs(save_path)

print("\n🚀 Hole deine komplette Lieblingssongs-Liste von Spotify...\n")

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
        time.sleep(1)  # Kleine Pause zwischen den Downloads, um die API nicht zu überlasten

    offset += limit

print("\n🎉 Fertig! Alle Songs wurden verarbeitet und gespeichert.")
