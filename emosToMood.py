import numpy
import pandas as pd
import numpy as np
from numpy import genfromtxt

GAMMA = 0.1
# df = pd.read_csv(DB_FILE)
# emo_vecs = [eval(','.join(vec.split())) for vec in df.loc[:, 'mood_vec']]
# songs = zip(df.loc[:, 'song_id'], emo_vecs)


class emoToMoodModel:

    def __init__(self, in_size, out_size, load_from_file=False):
        self.mat: np.matrix = np.mat((out_size, in_size))
        # self.d_file = d_file

        if load_from_file:
            self._load_mat()

        self.in_size = in_size
        self.out_size = out_size

        self.gamma = GAMMA

    def _load_mat(self, user='general'):
        self.mat = genfromtxt('mat.csv', delimiter=',')

    def _save_mat(self):
        # here I receive a matrix from Itamar! (self.mat should be replaced)
        numpy.savetxt('mat.csv', self.mat, delimiter=",")

    def fit(self, emos, exp, save=True):
        for em, ex in zip(emos, exp):
            self.mat -= self.gamma * self.gradient(em, ex)
        if save:
            self._save_mat()

    def gradient(self, emos, exp):
        g = np.zeros_like(self.mat)
        for r in self.out_size:
            camp = sum([self.mat[r][c] * emos[c] for c in self.in_size]) - exp[r]
            for c in self.mat[r]:
                g[r][c] = 2 * emos[c] * camp  # the derivative according to the var mat[r][c]
        return g

    def predict(self, emos):
        # (7, 4) * (4, 1)
        return self.mat.dot(emos.T)

weights_file = 'trined_models/emo_weights.csv'

emos_order = ['happy', 'sad', 'angry', 'neutral']
mood_order = ['happy', 'sad', 'energetic', 'calm']

qa='what would you like to listen when you'
songs=['Someone Like You, Adele','All of Me, John Legend','Slow Hands, Niall Horan']
songs+=['Only Human, Jonas Brothers','Growing Pains, Alessia Cara','Survivor, Destiny\'s Child']
songs+=['Havana, Instrumental Version','Can\'t Help Falling In Love, Kina Grannis']


def quiz():

    print(qa,' happy?')
    song = input(songs).split(',')
    df: pd.DataFrame = pd.read_csv('DB_FILE')



def emosToMoodDumb(emos):
    '''
    convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    '''
    return {'happy': emos['happy'], 'sad': emos['sad'], 'energetic': emos['angry'] + emos['happy'],
            'calm': emos['neutral']}


def emosToMood(emos):
    t = emosToMoodDumb(emos)
    print(t)
    return t
    # df = pd.read_csv(weights_file)
    # mtx = df.to_numpy()
    # '''
    # convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    # to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    # :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    # :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    # '''
    # mood_d = {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    # i = 0
    # for e in mood_d.keys():
    #     mood_d[e] = sum([int(mtx[j][i]) * emos[emos_order[j]] for j in range(4)])
    #     i += 1
    # return mood_d

# a = emoToMood
# a.__init__(a, 'mat.csv', 1, 2)
# a._save_mat(a)