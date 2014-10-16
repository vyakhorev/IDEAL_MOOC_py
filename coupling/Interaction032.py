from coupling.Interaction031 import c_Interaction031

class c_Interaction032(c_Interaction031):
    """
    An Interaction032 is an Interaction031
    that has a list of alternate interactions.
    """
    def __init__(self, label):
        super(c_Interaction032, self).__init__(label)
        self.alternateInteractions = []

    def addAlternateInteraction(self, interaction):
        if not(interaction in self.alternateInteractions):
            self.alternateInteractions += [interaction]

    def getAletnerateInteractions(self):
        return self.alternateInteractions