import numpy as np
import emosToMood as etm


class UserLearner:

    def __init__(self, load=False, user_name='') -> object:
        '''
        :param load: loading model parameters if True
        :param user_name: current user name
        '''
        self.user_name=user_name
        self.model = etm.EmoToMoodModel(7, 4, load_from_file=load, user_name=user_name)

    def learn_user(self, data_source):
        '''
        using data_source to learn the user
        :param data_source: callable object (str) -> tuple(list,list) returns user learning data
        '''
        emos, exp = data_source(self.user_name)
        self.model.fit(emos, exp)

    def emoToMood(self, emos:dict):
        '''
        :param emos: vector of face emotion
        :return: cast vector of emotion to vector of mood
        '''
        return self.model.predict(np.array(list(emos.values())))
