import numpy as np

import emosToMood as etm
from gui import ui_first_time


class userLearner:

    def __init__(self, load=False, userName='') -> object:
        self.model = etm.emoToMoodModel(7, 4, load_from_file=load, userName=userName)

    def learn_user(self, data_source=ui_first_time.ui_first_time):
        emos, exp = data_source()
        self.model.fit(emos, exp)

    def emoToMood(self, emos:dict):
        return self.model.predict(np.array(list(emos.values())))
