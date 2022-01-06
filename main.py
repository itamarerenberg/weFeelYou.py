import detectEmotions
from data_base import songs_db_maneger, users_db_maneger
import fitToUser as ftu

PL_SIZE = 20


def is_user_exist(userName):
    '''
    check if the user exists
    :param userName: current user name
    :return: True if exists
    '''
    return users_db_maneger.is_user_exist(userName)


def fit_playlist(face_pic, user_name):
    '''
    :param face_pics: image of a face
    :return: playlist of songs suitable to the image's face mood
    '''
    caster = ftu.UserLearner(load=True, user_name=user_name)

    pic_emos = detectEmotions.getEmotions(face_pic)  # returns a dict like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    dominant_emo = 0
    dominant_emo_val = 0
    for emo in pic_emos.keys():  # pick the dominant emotion
        if pic_emos[emo] > dominant_emo_val:
            dominant_emo_val = pic_emos[emo]
            dominant_emo = emo
    print(dominant_emo) # print for debug
    mood = caster.emoToMood(pic_emos) # cast the vector of emotion (len=7) to vector of mood (len=4)
    pl = songs_db_maneger.fit_k_songs(PL_SIZE, mood, user_name=user_name)
    return pl


def add_pl_to_db(pl_id, user_name):
    '''
    adds all the songs in the given playlist to the system's db
    :param pl_id: id of the playlist to add
    '''
    songs_db_maneger.add_songs_to_db(pl_id, user_name)

def new_user(user_name):
    """
    register a new user and displays a quiz for learning the new user
    :param user_name: new user's name
    :return: True, None if the user register successful and False, reason (string) otherwise
    """
    stat = users_db_maneger.add_user(userName=user_name)
    if stat[0]:
        caster = ftu.UserLearner(load=False, user_name=user_name)
        caster.learn_user()
    return stat

def dsource():
    '''
    helper function for debug
    '''
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

