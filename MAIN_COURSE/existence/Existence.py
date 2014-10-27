"""
 An c_Existence is an Object that simulates a "stream of intelligence" when it is run step by step.
 Each call to the Step() method generates an "event of intelligence" that can be traced.
 """

class c_Existence(object):
    #interface - abstract class, useless for Python
    """
    Perform one step of a "stream of intelligence".
    @return: a string representing the "event of intelligence" that was performed.
    """
    def step(self):
        pass
