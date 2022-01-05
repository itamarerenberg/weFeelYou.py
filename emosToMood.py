import numpy
import pandas as pd
import numpy as np
from numpy import genfromtxt
import os


USERS_MATS_DIR = './data_base/data/trained_models/users_mats'


GAMMA = 0.1

class emoToMoodModel:

    # convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    # to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    # :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    # :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    def __init__(self, in_size, out_size, load_from_file=False, userName=''):
        self.mat: np.matrix = np.zeros((out_size, in_size))
        # self.d_file = d_file
        self.userName = userName
        if load_from_file:
            self._load_mat()

        self.in_size = in_size
        self.out_size = out_size

        self.gamma = GAMMA

    def _load_mat(self, user='general'):
        self.mat = genfromtxt(f'{USERS_MATS_DIR}/({self.userName})mat.csv', delimiter=',')

    def _save_mat(self):
        numpy.savetxt(f'{USERS_MATS_DIR}/({self.userName})mat.csv', self.mat, delimiter=",")

    def fit(self, emos, exp, save=True):
        for em, ex in zip(emos, exp):
            self.mat -= self.gamma * self.gradient(em, ex)
        if save:
            self._save_mat()

    def gradient(self, emos, exp):
        g = np.zeros_like(self.mat)
        for r in range(self.out_size):
            camp = sum([self.mat[r][c] * emos[c] for c in range(self.in_size)]) - exp[r]
            for c in range(self.in_size):
                g[r][c] = 2 * emos[c] * camp  # the derivative according to the var mat[r][c]
        return g

    def predict(self, emos):
        # (7, 4) * (4, 1)
        return self.mat.dot(emos.T)




# def emosToMoodDumb(emos):
#     '''
#     convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
#     to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
#     :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
#     :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
#     '''
#     return {'happy': emos['happy'], 'sad': emos['sad'], 'energetic': emos['angry'] + emos['happy'],
#             'calm': emos['neutral']}
