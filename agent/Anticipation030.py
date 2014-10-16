from coupling.Interaction030 import c_Interaction030

"""
An Anticipation030 is created for each proposed primitive interaction.
An Anticipation030 is greater than another if its interaction has a greater valence than the other's.
"""

class c_Anticipation030(object):
    def __init__(self, an_interaction):
        self.interaction = an_interaction

    def getInteraction(self):
        return self.interaction

    def __cmp__(self, other):
        #we need this for sorting
        a = self.getInteraction().getValence()
        b = other.getInteraction().getValence()
        return a.__cmp__(b)  #this is just if a>b then 1 else 0

    def __eq__(self, other):
        #if you implement __cmp__ you should implement __eq__
        a = other.getInteraction().getValence()
        b = self.getInteraction().getValence()
        return a==b  #this is either true or false


