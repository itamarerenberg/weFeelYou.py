import numpy
import numpy as np
from numpy import genfromtxt

USERS_MATS_DIR = './data_base/data/trained_models/users_mats'

GAMMA = 0.1


class EmoToMoodModel:

    def __init__(self, in_size, out_size, load_from_file=False, user_name=''):
        '''
        :param in_size: length of origin vector
        :param out_size: length of destination vector
        :param load_from_file: loading model parameters if True
        :param user_name: current user name
        '''

        self.mat: np.matrix = np.zeros((out_size, in_size))
        self.userName = user_name
        if load_from_file:
            self._load_mat()
        self.in_size = in_size
        self.out_size = out_size
        self.gamma = GAMMA # learning rate

    def _load_mat(self):
        '''
        :return: loads the user model parameters
        '''
        self.mat = genfromtxt(f'{USERS_MATS_DIR}/({self.userName})mat.csv', delimiter=',')

    def _save_mat(self):
        '''
        :return: saves the user model parameters
        '''
        numpy.savetxt(f'{USERS_MATS_DIR}/({self.userName})mat.csv', self.mat, delimiter=",")

    def fit(self, emos, exp, save=True):
        '''
        :param emos: origin vector
        :param exp: expected destination vector
        :param save: saves the user model parameters if True
        '''
        for em, ex in zip(emos, exp):
            self.mat -= self.gamma * self.gradient(em, ex)
        if save:
            self._save_mat()

    def gradient(self, emos, exp):
        '''
        calculate the current gradient of the euclidean distance between exp and the model prediction for emos
        :param emos: origin vector
        :param exp: expected destination vector
        :return: gradient
        '''
        g = np.zeros_like(self.mat)
        for r in range(self.out_size):
            camp = sum([self.mat[r][c] * emos[c] for c in range(self.in_size)]) - exp[r]
            for c in range(self.in_size):
                g[r][c] = 2 * emos[c] * camp  # the derivative according to the var mat[r][c]
        return g

    def predict(self, emos):
        '''
        :param emos: origin vector
        :return: prediction destination vector for the origin vector
        '''
        return self.mat.dot(emos.T)  # (7, 4) * (4, 1)


def emosToMoodDumb(emos):
    '''
    convert a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    to a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    :param emos: a dict of emotions like {‘angry’: 0.0, ‘disgust’: 0.0, ‘fear’: 0.0, ‘happy’: 1.0, ‘sad’: 0.0, ‘surprise’: 0.0, ‘neutral’: 0.0}
    :return: a dict like  {'happy': 0, 'sad': 0, 'energetic': 0, 'calm': 0}
    '''
    return {'happy': emos['happy'], 'sad': emos['sad'], 'energetic': emos['angry'] + emos['happy'],
            'calm': emos['neutral']}
