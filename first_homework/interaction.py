from shared import *

class c_intercation(hashable):
    def __init__(self, label):
        self.label = label
        self.experience = None
        self.result = None
        self.valence = 0

    def __repr__(self):
        return self.label

    def set_experience(self, exp):
        self.experience = exp

    def get_experience(self):
        return self.experience

    def set_result(self, res):
        self.result = res

    def get_result(self):
        return self.result

    def set_valence(self, valence):
        self.valence = valence

    def get_valence(self):
        return self.valence