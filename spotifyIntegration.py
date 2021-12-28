import spotipy
from spotipy import SpotifyClientCredentials, util

client_id = '2c8552357e514360a36acfefaebebbed'
client_secret = 'ff7ec84eed7d4e1cb786a6ba949b1254'
redirect_uri = 'http://feelthemusic.com/callback/'
username = 'jkcltlydurh13jqp14n7ki73p'
scope = 'playlist-modify-public'
# Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)

# Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc.
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
spt = spotipy.Spotify(auth=token)


def get_song_name(song_id):
    meta = sp.track(song_id)
    return meta['name']


def get_song_artists(song_id):
    meta = sp.track(song_id)
    artists = meta['artists']
    artists_str = ''
    for artist in artists:
        artists_str += ' ' + artist['name']
    return artists_str


def get_song_album_name(song_id):
    meta = sp.track(song_id)
    return meta['album']['name']


def get_song_popularity(song_id):
    meta = sp.track(song_id)
    return meta['popularity']


def get_song_release_date(song_id):
    meta = sp.track(song_id)
    return meta['album']['release_date']


def get_song_feature(song_id):
    meta = sp.track(song_id)
    features = sp.audio_features(song_id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    ids = meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
             energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness',
               'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']
    return track, columns


def get_pl_songs(pl_id):
    playlist = spt.playlist_tracks(pl_id, limit=100)
    songs = []
    for song in playlist['items']:
        songs += [song['track']['id']]
    return songs