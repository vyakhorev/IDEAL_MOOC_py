from coupling.Interaction030 import c_Interaction030

class c_Interaction031(c_Interaction030):
    def __init__(self, label):
        super(c_Interaction031, self).__init__(label)
        self.weight = 0

    def getWeight(self):
        return self.weight

    def incrementWeight(self):
        self.weight += 1

    def __repr__(self):
        return self.getLabel() + " valence " + str(self.getValence()) + " weight " + str(self.weight)
