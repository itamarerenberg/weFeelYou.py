import pandas as pd
import knn
import spotifyIntegration
import quantifySong

USERS_SONGS_DIR = 'data_base/data/users_songs'


def fit_k_songs(pl_size, mood_vec, user_name):
    '''
    :param pl_size: size of the desired playlist
    :param mood_vec: vector of mood to fit a playlist to
    :return: url of spotify playlist of most suitable songs to the pic_mood with size of pl_size
    '''

    # load the user songs file
    df = pd.read_csv(f'{USERS_SONGS_DIR}/({user_name})songs.csv')
    emo_vecs = list(zip(df['calm'], df['energetic'], df['happy'], df['sad']))
    songs = list(zip(df.loc[:, 'id'], emo_vecs))
    songs = knn.knn(pl_size, songs, mood_vec)
    pl = spotifyIntegration.create_playlist('My Emotional Playlist1', songs)
    url = pl['external_urls']['spotify']
    return url


def add_multiple_playlists(pl_ids, user_name):
    '''
    :param pl_ids: playslists ids
    :param user_name: current user_name
    '''
    for pl in pl_ids.split('\n'):
        add_songs_to_db(pl, user_name)


def add_songs_to_db(pl_id, userName):
    '''
    Quantified and add all the songs in a playlist to the system's DB
    :param pl_id: playlist's id
    '''
    songs_id = spotifyIntegration.get_pl_songs(pl_id)
    songs_vecs = [list(quantifySong.predict_mood(song_id)) for song_id in songs_id]
    calm=[round(vec[0],12) for vec in songs_vecs]
    energetic=[round(vec[1],12) for vec in songs_vecs]
    happy=[round(vec[2],12) for vec in songs_vecs]
    sad=[round(vec[3],12) for vec in songs_vecs]
    songs_name= [spotifyIntegration.get_song_name(song_id) for song_id in songs_id]
    songs_artists= [spotifyIntegration.get_song_artists(song_id) for song_id in songs_id]
    songs_album=[spotifyIntegration.get_song_album_name(song_id) for song_id in songs_id]
    songs_release_date=[spotifyIntegration.get_song_release_date(song_id) for song_id in songs_id]
    songs_popularity=[spotifyIntegration.get_song_popularity(song_id) for song_id in songs_id]
    new_songs_df = pd.DataFrame({'id': songs_id, 'calm': calm,'energetic':energetic,'happy':happy,'sad':sad, 'name':songs_name, 'artists': songs_artists,'album':songs_album,'release_date':songs_release_date,'popularity':songs_popularity})
    # load the current songs file
    try:
        df: pd.DataFrame = pd.read_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv')
        df = df.append(new_songs_df).drop_duplicates(['id'])
    except pd.errors.EmptyDataError: # file empty
        df = new_songs_df
        pass
    except FileNotFoundError: # file hasn't created yet
        df = new_songs_df
        pass
    df.to_csv(f'{USERS_SONGS_DIR}/({userName})songs.csv', index=False)


def get_k_most(k, mood, user_name):
    '''
    :param k: number of songs
    :param mood: mood
    :param user_name: current user_name
    :return: k songs sorted by column mood with the biggest mood value
    '''
    if user_name is None:
        df = pd.read_csv(f'{USERS_SONGS_DIR}/songs1.csv')
        print("WARNING: get_k_most: user_name = None")
    else:
        try:
            df = pd.read_csv(f'{USERS_SONGS_DIR}/({user_name})songs.csv')
        except FileNotFoundError:
            df = pd.read_csv(f'{USERS_SONGS_DIR}/songs1.csv')
            print(f'WARNING: {user_name} songs file not found')
    kMostDf = df.sort_values(by=[mood], ignore_index=True, ascending=False)[:k]
    kMost = []
    for row in kMostDf.iterrows():
        kMost.append(dict(row[1]))
    return kMost


def create_new_songs_file(fileName):
    '''
    create new csv file in the songs files directory
    :param fileName:
    :return:
    '''
    songs_file_path = f'{USERS_SONGS_DIR}/{fileName}'
    new_songs_df = pd.DataFrame(
        {'id': [], 'calm': [], 'energetic': [], 'happy': [], 'sad': [], 'name': [],
         'artists': [], 'album': [], 'release_date': [],
         'popularity': []})
    new_songs_df.to_csv(songs_file_path)


if __name__ == '__main__':
    df = pd.read_csv(f'{USERS_SONGS_DIR}/(general)songs.csv')
    emo_vecs = list(zip(df['calm'], df['energetic'], df['happy'], df['sad']))
    print(emo_vecs)