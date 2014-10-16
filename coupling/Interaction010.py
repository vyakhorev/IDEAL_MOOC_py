from coupling.Interaction import c_Intercation

class c_Interaction010(c_Intercation):
    """ Inheritance instead of implementation of an interface
    in this example, "Interaction" in the brackets does nothing. You may erase it."""
    def __init__(self, label):
        #All these variables are directly available from outside (you may not use get/set).
        #Still, I keep the get/set to comply with Java example
        self.label = label
        self.experience = None  #Experience type here
        self.result = None      #c_Result type here

    def __repr__(self):
        # this is called with str() and print() with an instance of a class
        return str(self.experience) + str(self.result)

    def getLabel(self):
        return self.label

    def getExperience(self):
        return self.experience

    def setExperience(self, an_experiment):
        self.experience = an_experiment

    def getResult(self):
        return self.result

    def setResult(self, a_result):
        self.result = a_result

