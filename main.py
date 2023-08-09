import os
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print("Welcome to the Musical Time Machine!")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date = "2000-08-12"
year = date.split('-')[0]

count = 1
songs = {
    f"{count}": ["title", "artist"]
}

# Scrape the Billboard TOP 100
response = requests.get(f"https://www.billboard.com/charts/hot-100/2000-08-12/")
soup = BeautifulSoup(response.text, "html.parser")

# Find the first song details
top_song_container = soup.find(name="h3",
                               class_="c-title a-font-primary-bold-l a-font-primary-bold-m@mobile-max lrv-u-color"
                                      "-black u-color-white@mobile-max lrv-u-margin-r-150")
top_song = top_song_container.findChild().text.strip()

top_song_artist_container = soup.find(name="p",
                                      class_="c-tagline a-font-primary-l a-font-primary-m@mobile-max "
                                             "lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 "
                                             "lrv-u-padding-t-025 lrv-u-margin-r-150")
top_song_artist = top_song_artist_container.text

songs[f"{count}"] = [top_song, top_song_artist]

# Add the rest of the songs
songs_container = soup.find_all(name="h3",
                                class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                       "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                       "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                       "u-max-width-230@tablet-only")
for song in songs_container:
    count += 1
    songs[f"{count}"] = ["", ""]
    songs[f"{count}"][0] = song.text.strip()

# Add the rest of the song artists
artists_container = soup.find_all(name="span",
                                  class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                                         "u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block "
                                         "a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")
count = 1

for artist in artists_container:
    count += 1
    songs[f"{count}"][1] = artist.text.strip()

# Authentication with Spotify
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ['SPOTIFY_CLIENT_ID'],
        client_secret=os.environ['SPOTIFY_CLIENT_SECRET'],
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = spotify.current_user()["id"]
print(user_id)

# Search Spotify for the Songs
songs_uri = []
for key, value in songs.items():
    result = spotify.search(q=f"track: {value[0]} year: {year}", type='track', market='PH')

    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"v{value[0]} doesn't exist in Spotify. Skipped")

# Creating the Playlists on Spotify

# Adding Songs to the Playlist
