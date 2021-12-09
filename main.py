import spotifyIntegration

import demoFuncs
import detectEmotions
import emosToMood
import songs_db_maneger
import time
import cv2
from PIL import Image
import base64
import io
import numpy as np
# import torch
#
#
#
#
# def base64tondarray(img):
#     base64_decoded = base64.b64decode(img)
#     image = Image.open(io.BytesIO(base64_decoded))
#     image_np = np.array(image)
#     image_torch = torch.tensor(np.array(image))
#
#

PL_SIZE = 10


def fit_playlist(face_pic):
    '''
    :param face_pics: list of picture of a face
    :return: playlist of songs suitable to the pictures's face mood
    '''
    pic_emos = detectEmotions.getEmotions(face_pic)  # returns a dict like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    domino_emo = 0
    dominon_emo_val = 0
    for e in pic_emos.keys():
        if pic_emos[e] > dominon_emo_val:
            dominon_emo_val = pic_emos[e]
            domino_emo = e
    print(domino_emo)
    mood = emosToMood.emosToMood(pic_emos)
    pl = songs_db_maneger.fit_k_songs(PL_SIZE, mood)
    return pl


def add_pl_to_db(pl_id):
    '''
    adds all the songs in the songs in the given playlist to the system's db
    :param pl_id: id of the playlist to add
    '''
    songs_db_maneger.add_songs_to_db(pl_id)


# pl_id = 'spotify:playlist:37i9dQZF1E3a3sxiJLF0ZI'
# add_pl_to_db(pl_id)
face_pic = demoFuncs.takePicture()
ids_pl = fit_playlist(face_pic)
for s_id in ids_pl:
    print(spotifyIntegration.get_song_name(s_id), "https://open.spotify.com/track/" + s_id)#, ' by: ', spotifyIntegration.get_song_artists(s_id))
# pl = []
# for s_id in ids_pl:
#     pl.append(spotifyIntegration.get_song_name(s_id))
# print(pl)
