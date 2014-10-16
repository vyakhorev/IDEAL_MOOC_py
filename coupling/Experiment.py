"""
An experiment that can be chosen by the agent.
This is also called "experience" everywhere
"""

class c_Experiment():
    def __init__(self, label):
        self.label = label  #The experience's label.

    def __repr__(self):
        return "experience:" + self.label  + " "

    def getLabel(self):
        return self.label
