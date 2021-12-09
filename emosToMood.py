import pandas as pd


weights_file = 'trined_models/emo_weights.csv'


emos_order = ['happy', 'sad', 'angry', 'neutral']
mood_order = ['happy', 'sad', 'energetic', 'calm']


def emosToMood1(emos):
    '''
    convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    '''
    return {'happy': emos['happy'], 'sad': emos['sad'], 'energetic': emos['angry'] + emos['happy'], 'calm': emos['neutral']}


def emosToMood(emos):
    df = pd.read_csv(weights_file)
    mtx = df.to_numpy()
    '''
    convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    '''
    mood_d = {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    i = 0
    for e in mood_d.keys():
        mood_d[e] = sum([int(mtx[j][i]) * emos[emos_order[j]] for j in range(4)])
        i += 1
    return mood_d