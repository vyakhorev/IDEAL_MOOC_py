from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction032 import c_Interaction032
from existence.Existence031 import c_Existence031
from agent.Anticipation032 import c_Anticipation032

class c_Existence032(c_Existence031):
    def step(self):
        anticipations = self.anticipate()
        intendedInteraction = self.selectInteraction(anticipations)
        experience = intendedInteraction.getExperience()
        #Change the call to the function returnResult to change the environment
        #result = self.returnResult010(experience)
        #result = self.returnResult030(experience)
        result = self.returnResult031(experience)
        enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
        print("Enacted "+ str(enactedInteraction))
        if enactedInteraction != intendedInteraction:
            intendedInteraction.addAlternateInteraction(enactedInteraction)
            print("Alternate " + str(enactedInteraction))
        if enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        self.learnCompositeInteraction(enactedInteraction)
        self.setEnactedInteraction(enactedInteraction)
        return self.getMood()

    def selectInteraction(self, anticipations):
        anticipations.sort()
        for anticipation in anticipations:
            print("anticipate " + str(anticipation))
        selectedAnticipation = anticipations[0]
        intendedInteraction = selectedAnticipation.getInteraction()
        return intendedInteraction

    def anticipate(self):
        #Computes the list of anticipations
        anticipations = self.getDefaultAnticipations()
        activatedInteractions = self.getActivatedInteractions()
        for activatedInteraction in activatedInteractions:
            proposedInteraction = activatedInteraction.getPostInteraction()
            proclivity = activatedInteraction.getWeight() * proposedInteraction.getValence()
            anticipation = c_Anticipation032(proposedInteraction, proclivity)
            if anticipation in anticipations: #if there are any with the same experience (same object of type Experiment)
                i = anticipations.index(anticipation)
                anticipations[i].addProclivity(proclivity)
            else:
                anticipations.add(anticipation)
        for anticipation in anticipations:
            for interaction in anticipation.getInteraction().getAletnerateInteractions():
                for activatedInteraction in activatedInteractions:
                    if interaction == activatedInteraction.getPostInteraction():
                        proclivity = activatedInteraction.getWeight() * interaction.getValence()
                        anticipation.addProclivity(proclivity)
        return anticipations

    def getDefaultAnticipations(self):
        anticipations = []
        for interaction in self.interactions.itervalues():
            if interaction.isPrimitive():
                anticipation = c_Anticipation032(interaction, 0)
                anticipations += [anticipation]
        return anticipations

    def createInteraction(self, label):
        return c_Interaction032(label)


