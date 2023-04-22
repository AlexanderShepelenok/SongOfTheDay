import spotipy
import requests
import urllib.parse
import sys
from googleapiclient.discovery import build

# Authenticate with the Spotify API using your client ID and client secret
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(client_id='SPOTIFY_CLIENT_ID', client_secret='SPOTIFY_CLIENT_SECRET'))

# Authenticate with the YouTube Data API using your API key
youtube = build('youtube', 'v3', developerKey='YOUTUBE_DEV_KEY')

class SpotifyData:
    def __init__(self, link, cover, album, year, hashtags):
        self.link = link
        self.cover = cover
        self.album = album
        self.year = year
        self.hashtags = hashtags
    

# Search for the song on Spotify
def search_spotify(artist, track):
    result = sp.search(q=f'artist:{artist} track:{track}', type='track', limit=1)
    if result['tracks']['items']:
        track_info = result['tracks']['items'][0]
        track_id = track_info['id']
        album_info = track_info['album']
        album_name = album_info['name']
        release_year = album_info['release_date'][0:4]
        album_cover_link = album_info['images'][0]['url']
        spotify_link = f'https://open.spotify.com/track/{track_id}'

        artist_uri = track_info['artists'][0]['uri']
        artist_data = sp.artist(f'{artist_uri}')
        genres = artist_data['genres']
        hashtags = ['#' + genre.replace(' ', '') for genre in genres]
        hashtags_string = ' '.join(hashtags)
        return SpotifyData(spotify_link, album_cover_link, album_name, release_year, hashtags_string)
    else:
        return None

# Search for the song on YouTube
def search_youtube(artist, track):
    query = f'{artist} {track}'
    search_response = youtube.search().list(q=query, type='video', part='id,snippet', maxResults=1).execute()
    if search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        youtube_link = f'https://www.youtube.com/watch?v={video_id}'
        return youtube_link
    else:
        return None

# Search for the song on Yandex.Music (there is no public doc for this API by the way)
def search_yandex(artist, track):
    query = f'{artist}-{track}'
    encoded_query = urllib.parse.quote(query)
    response = requests.get(f'https://music.yandex.ru/handlers/music-search.jsx?text={encoded_query}&type=tracks')
    if response.status_code == 200:
        data = response.json()
        if data['tracks']['items']:
            track_id = data['tracks']['items'][0]['id']
            yandex_link = f'https://music.yandex.ru/track/{track_id}'
            return yandex_link
        else:
            return None
    else:
        return None

if len(sys.argv) < 3:
    print('Usage: python songoftheday.py <artist> <track>')
else:
    artist = sys.argv[1]
    track = sys.argv[2]
    spotify_data = search_spotify(artist, track)
    youtube_link = search_youtube(artist, track)
    yandex_link = search_yandex(artist, track)

    print(f'#songoftheday {artist} - {track}')
    print(f'💽 {spotify_data.album} ({spotify_data.year})')
    print(f'🩻 {spotify_data.cover} {spotify_data.hashtags}\n')
    print(f'🟢 Spotify: {spotify_data.link}')
    print(f'🟡 Yandex.Music: {yandex_link}')
    print(f'🔴 YouTube: {youtube_link}')