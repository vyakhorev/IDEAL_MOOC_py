from coupling.Experiment import c_Experiment


class c_Experiment040(c_Experiment):
    # The experience's interaction
    def __init__(self, label):
        super(c_Experiment040, self).__init__(label)
        self.intendedInteraction = None
        self.isAbstract = 1

    def resetAbstract(self):
        self.isAbstract = 0

    def setIntendedInteraction(self, intendedInteraction):
        self.intendedInteraction = intendedInteraction

    def getIntendedInteraction(self):
        return self.intendedInteraction

