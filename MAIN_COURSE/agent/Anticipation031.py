import coupling.Experiment

class c_Anticipation031():
    """
    An Anticipation031 is created for each experience.
    Anticipations031 are equal if they propose the same experience.
    An Anticipation031 is greater than another if its proclivity is greater that the other's.
    """
    def __init__(self, experience, proclivity):
        self.experience = experience
        self.proclivity = proclivity

    def __cmp__(self, other):
        #we need this for sorting
        a = self.getProclivity()
        b = other.getProclivity()
        return a.__cmp__(b)  #just a comparition of numbers

    def __eq__(self, other):
        #This is strange - use one thing for __cmp__ and other thing for __eq__.. I mean, not flexible.
        a = self.getExperience()
        b = other.getExperience()
        #a and b are Experiments, there is no __cmp__ in Experiment, so we are checking that the memory links are the same
        return a == b

    def getExperience(self):
        return self.experience

    def setExperience(self, experience):
        self.experience = experience

    def getProclivity(self):
        return self.proclivity

    def addProclivity(self, proclivity):
        self.proclivity += proclivity

    def __repr__(self):
        return self.experience.getLabel() + " proclivity " + str(self.proclivity)

