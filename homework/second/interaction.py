from shared import *

class c_intercation(hashable):
    def __init__(self, label):
        self.label = label
        self.experience = None
        self.result = None
        self.pre_interaction = None
        self.post_interaction = None
        self.valence = 0

    def __repr__(self):
        if self.is_primitive():
            return ("[%s -> %s v: %d]"% (str(self.experience), str(self.result), self.valence))
        else:
            return ("[%s ---> %s]"% (str(self.pre_interaction), str(self.post_interaction)))

    def is_primitive(self):
        if self.pre_interaction is None and self.post_interaction is None:
            return 1





