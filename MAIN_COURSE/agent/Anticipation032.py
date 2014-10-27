from agent.Anticipation030 import c_Anticipation030

class c_Anticipation032(c_Anticipation030):
    def __init__(self, interaction, proclivity):
        super(c_Anticipation032, self).__init__(interaction)
        self.proclivity = proclivity

    def __cmp__(self, other):
        a = self.getProclivity()
        b = other.getProclivity()
        return a.__cmp__(b)  #just a comparition of numbers

    def __eq__(self, other):
        a = self.getInteraction()
        b = other.getInteraction()
        return a == b  #this a call for above method __cmp__(a, b)

    def getProclivity(self):
        return self.proclivity

    def addProclivity(self, proclivity):
        self.proclivity += proclivity

    def __repr__(self):
        return self.getInteraction().getLabel() + " proclivity " + str(self.getProclivity())