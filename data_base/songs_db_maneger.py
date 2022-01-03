import os.path
import webbrowser

import pandas as pd
import spotipy

import knn
import quantefySong
import spotifyIntegration


USERS_SONGS_DIR = 'data_base/data/users_songs'


def fit_k_songs(pl_size, mood_vec, userName='general'):
    '''
    :param pl_size: size of the desired playlist
    :param pic_mood: picture to fit a playlist to
    :return: playlist of 'pl_size' most suitable songs to the pic_mood
    '''
    #  mood_vec = [pic_mood['calm'], pic_mood['energetic'], pic_mood['happy'], pic_mood['sad']]
    # load the song DB
    df = pd.read_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv')
    #todo list of float
    emo_vecs = list(zip(df['calm'], df['energetic'], df['happy'], df['sad']))
    songs = list(zip(df.loc[:, 'id'], emo_vecs))
    songs = knn.knn(pl_size, songs, mood_vec)
    pl = spotifyIntegration.create_playlist('My Emotional Playlist1', songs)
    # print('pl:',pl)
    url = pl['external_urls']['spotify']

    #webbrowser.open(url)
    return url



def add_songs_to_db(pl_id, userName='general'):
    '''
    Quantified and add all the songs in a playlist to the to the system's DB
    :param pl_id: playlist's id
    '''
    songs_id = spotifyIntegration.get_pl_songs(pl_id)
    songs_vecs = [list(quantefySong.predict_mood(song_id)) for song_id in songs_id]
    calm=[round(vec[0],8) for vec in songs_vecs]
    energetic=[round(vec[1],8) for vec in songs_vecs]
    happy=[round(vec[2],8) for vec in songs_vecs]
    sad=[round(vec[3],8) for vec in songs_vecs]
    songs_name= [spotifyIntegration.get_song_name(song_id) for song_id in songs_id]
    songs_artists= [spotifyIntegration.get_song_artists(song_id) for song_id in songs_id]
    songs_album=[spotifyIntegration.get_song_album_name(song_id) for song_id in songs_id]
    songs_release_date=[spotifyIntegration.get_song_release_date(song_id) for song_id in songs_id]
    songs_popularity=[spotifyIntegration.get_song_popularity(song_id) for song_id in songs_id]
    new_songs_df = pd.DataFrame({'id': songs_id, 'calm': calm,'energetic':energetic,'happy':happy,'sad':sad, 'name':songs_name, 'artists': songs_artists,'album':songs_album,'release_date':songs_release_date,'popularity':songs_popularity})
    df = 0
    try:
        df: pd.DataFrame = pd.read_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv')
        df = df.append(new_songs_df).drop_duplicates(['id'])
    except pd.errors.EmptyDataError:
        pass
    except FileNotFoundError:
        pass
    finally:
        df = new_songs_df
    df.to_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv', index=False)


def get_k_most(k, mood, userName=None):
    if userName is None:
        df = pd.read_csv(f'{USERS_SONGS_DIR}/songs1.csv')
    else:
        try:
            df = pd.read_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv')
        except FileNotFoundError:
            df = pd.read_csv(f'{USERS_SONGS_DIR}/songs1.csv')
            print(f'{userName} songs file not found')
    kMost = df.sort_values(by=[mood], ignore_index=True, ascending=False)
    return kMost


def create_new_songs_file(fileName):
    songs_file_path = f'{USERS_SONGS_DIR}/{fileName}'
    new_songs_df = pd.DataFrame(
        {'id': [], 'calm': [], 'energetic': [], 'happy': [], 'sad': [], 'name': [],
         'artists': [], 'album': [], 'release_date': [],
         'popularity': []})
    df.to_csv(songs_file_path)


if __name__ == '__main__':
    # list_pl=['spotify:playlist:0VQQOxFEEg3D7ufmCqp2v0','spotify:playlist:70wLHBSTHerQ7eaPP3yBfZ','spotify:playlist:4KKrfwLN6Ml5fb2YTE9kPP','spotify:playlist:6b2zNL2PGawMnlGsF1Bbca','spotify:playlist:37i9dQZF1EjxkSHsqu8Rod','spotify:playlist:22yAOa01NKIxxRMJzmwrDm','spotify:playlist:37i9dQZF1DXcBWIGoYBM5M','spotify:playlist:37i9dQZF1DXbYM3nMM0oPk','https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=88b8e7b09f2a4d30','spotify:playlist:37i9dQZF1DX4WYpdgoIcn6','spotify:playlist:37i9dQZF1DWTwnEm1IYyoj']
    # for pl in list_pl:
    #     add_songs_to_db(pl)
    df = pd.read_csv(f'{USERS_SONGS_DIR}/(general)songs.csv')
    emo_vecs = list(zip(df['calm'], df['energetic'], df['happy'], df['sad']))
    print(emo_vecs)