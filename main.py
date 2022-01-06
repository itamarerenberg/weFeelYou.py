import detectEmotions
from data_base import songs_db_maneger, users_db_maneger
import fitToUser as ftu

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

PL_SIZE = 20


def dsource():
    emos, exp = [], []
    for i in range(7):
        em = [0, 0, 0, 0, 0, 0, 0]
        ex = [0, 0, 0, 0]
        em[i] = 1
        ex[i % 4] = .5
        ex[(i + 2) % 4] = .25
        emos.append(em)
        exp.append(ex)
    return emos, exp


def is_user_exist(userName):
    return users_db_maneger.is_user_exist(userName)


def new_user(uName=''):
    """
    register a new user and displays a quiz for learning the new user
    :param uName: new user's name
    :return: True, None if the user register successful and False, reason (string) otherwise
    """
    stat = users_db_maneger.add_user(userName=uName)
    if stat[0]:
        caster = ftu.userLearner(load=False, userName=uName)
        caster.learn_user()
    return stat


def fit_playlist(face_pic=None, userName='general'):
    '''
    :param face_pics: list of picture of a face
    :return: playlist of songs suitable to the pictures's face mood
    '''
    caster = ftu.userLearner(load=True, userName=userName)
    # caster.learn_user()#data_source=dsource)

    pic_emos = detectEmotions.getEmotions(
        face_pic)  # returns a dict like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    domino_emo = 0
    dominon_emo_val = 0
    for e in pic_emos.keys():  # pick the dominate emotion
        if pic_emos[e] > dominon_emo_val:
            dominon_emo_val = pic_emos[e]
            domino_emo = e
    print(domino_emo)
    mood = caster.emoToMood(pic_emos)  # emosToMood.emosToMood(pic_emos)
    pl = songs_db_maneger.fit_k_songs(PL_SIZE, mood, userName=userName)
    return pl


def add_pl_to_db(pl_id, userName=''):
    '''
    adds all the songs in the songs in the given playlist to the system's db
    :param pl_id: id of the playlist to add
    '''
    songs_db_maneger.add_songs_to_db(pl_id, userName)

# pl_id = 'spotify:playlist:37i9dQZF1E3a3sxiJLF0ZI'
# add_pl_to_db(pl_id)
# face_pic = ui_capture_picture.take_picture()
# face_pic = demoFuncs.takePicture()


# print(fit_playlist(face_pic))
# fit_playlist(face_pic)
# for s_id in ids_pl:
#     print(spotifyIntegration.get_song_name(s_id), "https://open.spotify.com/track/" + s_id)#, ' by: ', spotifyIntegration.get_song_artists(s_id))
# pl = []
# for s_id in ids_pl:
#     pl.append(spotifyIntegration.get_song_name(s_id))
# print(pl)
