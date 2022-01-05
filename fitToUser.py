import numpy as np

import emosToMood as etm
from gui import  ui_main_window


class userLearner:

    def __init__(self, load=False, userName='') -> object:
        self.user_name=userName
        self.model = etm.emoToMoodModel(7, 4, load_from_file=load, userName=userName)

    def learn_user(self, data_source:callable(object)=ui_main_window.ui_first_time):
        emos, exp = data_source(self.user_name)
        self.model.fit(emos, exp)

    def emoToMood(self, emos:dict):
        return self.model.predict(np.array(list(emos.values())))
