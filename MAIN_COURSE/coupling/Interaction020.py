from coupling.Interaction010 import c_Interaction010

"""
An Interaction020 is an Interaction010 with a valence.
"""

class c_Interaction020(c_Interaction010):
    def __repr__(self):
        return self.getLabel() + "," + str(self.getValence())

    def setValence(self, valence):
        self.valence = valence

    def getValence(self):
        return self.valence

