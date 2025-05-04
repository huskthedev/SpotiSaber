# BeatSaver Map Downloader for Spotify Tracks

This script automatically downloads **Beat Saber** maps based on your **Spotify saved tracks**. It fetches your saved songs from Spotify and then uses the **BeatSaver API** to search for the first available map for each song in the format **Artist - Songname**. Once found, the map is downloaded and saved to a folder you specify.

## What Happens in the Script:
- **Spotify**: The script fetches your saved tracks using the **Spotify Web API**.
- **BeatSaver**: It uses the **BeatSaver API** to search for Beat Saber maps based on the `Artist - Songname` format.
- It will then automatically download the **first map found** for each song and save it to the folder you specify.

---

## What You Need to Do for Tokens:

### 1. **Spotify API Tokens**

To run this script, you need to obtain your **Spotify API tokens**. Here's how to do it:

#### **Create a Spotify Developer Account:**
- Go to [Spotify for Developers](https://developer.spotify.com/dashboard/applications).
- Log in with your Spotify account (or create one if you don't have one).

#### **Create a New Spotify App:**
- Click on **Create an App**.
- Name the app and provide a description.
- After creating the app, you'll be provided with a **Client ID** and **Client Secret**. Copy these, as you'll need them for the script.

#### **Set the Redirect URI:**
- In the Spotify Developer Dashboard, set the **Redirect URI** to:


- This URI is used by the OAuth flow to redirect after logging in.

### 2. **Install Required Libraries:**

You will need to install the required libraries for running the script:

```bash
pip install -r requirements.txt
