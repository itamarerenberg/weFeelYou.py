import pickle
import keras
import numpy as np
from spotifyIntegration import get_song_feature

model = 0
scaler = 0
loaded = False


def load_model():
    '''
    load the model of quantify songs
    '''
    global model
    global scaler
    global loaded
    model = keras.models.load_model('data_base/data/trained_models/music_clisifier_model')
    scaler = pickle.load(open('data_base/data/trained_models/scaler.pkl', 'rb'))
    loaded = True





def predict_mood(id_song):
    '''
    :param id_song: id of a song to predict
    :return: predicted vector of mood for the song
    '''
    if not loaded:
        load_model()
    # Obtain the features of the song (Function created on helpers.py)
    preds = get_song_feature(id_song)
    preds_arg = np.array(preds[0][6:-2]).reshape(1, -1)
    preds_arg = scaler.transform(preds_arg)
    return model.predict(preds_arg)[0]


load_model()