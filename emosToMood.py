import pandas as pd
import numpy as np


GAMMA = 0.1

class emoToMood:

    def __init__(self, d_file, in_size, out_size):
        self.mat: np.matrix = np.m((4, 7))
        self.d_file = d_file
        self._load_mat()

        self.in_size = in_size
        self.out_size = out_size

        self.gamma = GAMMA

    def _load_mat(self, user='general'):
        # self.mat = [loded vals]
        pass

    def _save_mat(self):
        saved_list = self.mat.d

        # np.ndarray((2,), buffer=np.array([1, 2, 3]),
        # offset = np.int_().itemsize,
        # dtype = int
        # save the 7X4 matrix (self.mat: np.ndarray)  of values of the model,
        pass

    def train(self, emos, exp):
        self.mat -= self.gamma * self.gradient(emos, exp)

    def gradient(self, emos, exp):
        g = np.zeros_like(self.mat)
        for r in self.out_size:
            camp = sum([self.mat[r][c] * emos[c] for c in self.in_size]) - exp[r]
            for c in self.mat[r]:
                g[r][c] = 2 * emos[c] * camp  # the derivative according to the var mat[r][c]
        return g


weights_file = 'trined_models/emo_weights.csv'


emos_order = ['happy', 'sad', 'angry', 'neutral']
mood_order = ['happy', 'sad', 'energetic', 'calm']


def emosToMoodDumb(emos):
    '''
    convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    '''
    return {'happy': emos['happy'], 'sad': emos['sad'], 'energetic': emos['angry'] + emos['happy'], 'calm': emos['neutral']}


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