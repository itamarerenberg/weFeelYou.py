import emosToMood as etm
import quiz


class userLearner:

    def __init__(self, load=False):
        self.model = etm.emoToMoodModel(7, 4, load_from_file=load)

    def learn_user(self, data_source=quiz.quiz):
        emos, exp = data_source()
        self.model.fit(emos, exp)

    def emoToMood(self, emos):
        return self.model.predict(emos)
