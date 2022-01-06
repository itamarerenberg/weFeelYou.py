import numpy as np

import emosToMood as etm
from gui import  main_gui


class userLearner:

    def __init__(self, load=False, userName='') -> object:
        self.user_name=userName
        self.model = etm.EmoToMoodModel(7, 4, load_from_file=load, user_name=userName)

    def learn_user(self, data_source):
        emos, exp = data_source(self.user_name)
        self.model.fit(emos, exp)

    def emoToMood(self, emos:dict):
        return self.model.predict(np.array(list(emos.values())))
