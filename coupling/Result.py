class c_Result():
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "result:" + self.label + " "

    def getLabel(self):
        return self.label