class c_Intercation(object):
    #interface - abstract class, useless for Python.
    #TODO: to make it more useful, one may throw exceptions here.
    def getLabel(self):
        #return the interaction's label
        pass    #should return a string

    def getExperience(self):
        #return the interaction's experience
        pass    #should return c_Experiment instance

    def getResult(self):
        #return the interaction's result
        pass    #should return c_Result instance

    def setExperience(self, an_experiment):
        # an_experiment is the interaction's experience.
        pass

    def setResult(self, a_result):
        # a_result is the interaction's result.
        pass

    def __hash__(self):
        #this allows any c_Intercation to serve as a key in a dict()
        return hash(self.label)

    def __eq__(x, y):
        #this is checked when the hash-codes are even
        if (y is not None) and (x is not None):
            return x.label == y.label