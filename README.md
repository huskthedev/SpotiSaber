What Happens in the Script:
Spotify: It fetches your saved tracks using the Spotify Web API.

BeatSaver: It uses the BeatSaver API to search for Beat Saber maps based on the Artist - Songname format.

It will then automatically download the first map found for each song and save it in the folder you specify.

What You Need to Do for Tokens:
To run the script, you'll need to get Spotify API tokens. Here's how you do it:

Create a Spotify Developer Account:

Go to Spotify for Developers.

Log in with your Spotify account (or create one if you don't have it yet).

Create a New Spotify App:

Click on Create an App.

Name it and provide a description.

You'll be given a Client ID and Client Secret. Copy them, as you'll need them in the script.

Set the Redirect URI:

In the Spotify Developer Dashboard, set the Redirect URI to:

arduino
Kopieren
Bearbeiten
http://127.0.0.1:8888/callback/
This URI is used by the OAuth flow to redirect after logging in.

Install Required Libraries:

You’ll need spotipy and requests to run the script. Install them using:

bash
Kopieren
Bearbeiten
pip install spotipy requests
Run the Script:

When you run the script, it will open a browser window asking for authorization. Log in to your Spotify account and approve the app to access your saved tracks.

Once authorized, the script will fetch your saved tracks and start downloading the maps automatically.

Read me was written by ai script was selfmade
