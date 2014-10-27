"""
An experiment that can be chosen by the agent.
This is also called "experience" everywhere
"""

class c_Experiment(object):
    def __init__(self, label):
        self.label = label  #The experience's label.

    def __repr__(self):
        return "experience:" + self.label  + " "

    def getLabel(self):
        return self.label
    
    def __hash__(self):
        #this allows c_Experiment to serve as a key in a dict()
        return hash(self.label)

    def __eq__(x, y):
        #this is checked when the hash-codes are even
        if (y is not None) and (x is not None):
            return x.label == y.label

