from coupling.Interaction020 import c_Interaction020

"""
An Interaction030 is an Interaction020 that can be primitive or composite
A composite interaction has a preInteraction and a postInteraction.
"""

class c_Interaction030(c_Interaction020):
    def __init__(self, label):
        super(c_Interaction030, self).__init__(label)  #just do not want to retype the thing in c_Interaction010
        self.preInteraction = None
        self.postInteraction = None

    def getPreInteraction(self):
        return self.preInteraction

    def setPreInteraction(self, preInteraction):
        self.preInteraction = preInteraction

    def getPostInteraction(self):
        return self.postInteraction

    def setPostInteraction(self, postInteraction):
        self.postInteraction = postInteraction

    def isPrimitive(self):
        return (self.getPreInteraction() is None)

