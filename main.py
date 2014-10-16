"""
Some examples for IDEAL MOOC on embodied AI

This is a copy of a Java code hosted via SVN:
http://developmental-learning-tutorial.googlecode.com/svn/trunk/TD/
"""

from existence.Existence010 import c_Existence010
from existence.Existence020 import c_Existence020
from existence.Existence030 import c_Existence030
from existence.Existence031 import c_Existence031
from existence.Existence032 import c_Existence032

__author__ = 'Vyakhorev'

class MainLoop():
    def __init__(self, exist_class):
        self.the_existence = exist_class()

    def existentialLoop(self, n=20):
        for i in xrange(0,n):
            step_trace = self.the_existence.step()
            print("[" + str(i) + "]: " + step_trace)
            #Uncomment if you feel curious:
            #print("\t interactions in memory: " + str(self.the_existence.interactions))

if __name__ == "__main__":
    #Uncomment one of "chosen_existence_class"
    chosen_existence_class = c_Existence010
    #chosen_existence_class = c_Existence020
    #chosen_existence_class = c_Existence030
    #chosen_existence_class = c_Existence031
    #chosen_existence_class = c_Existence032
    prgr = MainLoop(chosen_existence_class)
    prgr.existentialLoop()