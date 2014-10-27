class c_Result():
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "result:" + self.label + " "

    def getLabel(self):
        return self.label

    def __hash__(self):
        #this allows c_Result to serve as a key in a dict()
        return hash(self.label)

    def __eq__(x, y):
        #this is checked when the hash-codes are even
        if (y is not None) and (x is not None):
            return x.label == y.label