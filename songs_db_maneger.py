import pandas as pd
import knn
import quantefySong
import spotifyIntegration


DB_FILE = "songs.csv"


def fit_k_songs(pl_size, pic_mood):
    '''
    :param pl_size: size of the desired playlist
    :param pic_mood: picture to fit a playlist to
    :return: playlist of 'pl_size' most suitable songs to the pic_mood
    '''
    mood_vec = [pic_mood['calm'], pic_mood['energetic'], pic_mood['happy'], pic_mood['sad']]
    # load the song DB
    df = pd.read_csv(DB_FILE)
    emo_vecs = [eval(','.join(vec.split())) for vec in df.loc[:, 'mood_vec']]
    songs = zip(df.loc[:, 'song_id'], emo_vecs)

    songs = knn.knn(pl_size, songs, mood_vec)
    return songs


def add_songs_to_db(pl_id):
    '''
    Quantified and add all the songs in a playlist to the to the system's DB
    :param pl_id: playlist's id
    '''
    songs_id = spotifyIntegration.get_pl_songs(pl_id)
    songs_vecs = [quantefySong.predict_mood(song_id) for song_id in songs_id]
    new_songs_df = pd.DataFrame({'song_id': songs_id, 'mood_vec': songs_vecs})
    df = 0
    try:
        df: pd.DataFrame = pd.read_csv(DB_FILE)
        df = df.append(new_songs_df).drop_duplicates(['song_id'])
    except pd.errors.EmptyDataError:
        df = new_songs_df
    df.to_csv(DB_FILE, index=False)

