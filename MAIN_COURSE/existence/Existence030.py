from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction030 import c_Interaction030
from existence.Existence020 import c_Existence020
from agent.Anticipation030 import c_Anticipation030

"""
Existence030 is a sort of Existence020.
It learns composite interactions (Interaction030).
It bases its next choice on anticipations that can be made from reactivated composite interactions.
Existence030 illustrates the benefit of basing the next decision upon the previous enacted Interaction.
"""

class c_Existence030(c_Existence020):
    def initExistence(self):
        e1 = self.addOrGetExperience(self.LABEL_E1)
        e2 = self.addOrGetExperience(self.LABEL_E2)
        r1 = self.createOrGetResult(self.LABEL_R1)
        r2 = self.createOrGetResult(self.LABEL_R2)
        self.addOrGetPrimitiveInteraction(e1, r1, -1)
        self.addOrGetPrimitiveInteraction(e1, r2, 1)
        self.addOrGetPrimitiveInteraction(e2, r1, -1)
        self.addOrGetPrimitiveInteraction(e2, r2, 1)
        self.enactedInteraction = None
        self.previous_experience = None

    def step(self):
        anticipations = self.anticipate()
        experience = self.selectInteraction(anticipations).getExperience()
        #Change the call to the function returnResult to change the environment
        #result = self.returnResult010(experience)
        result = self.returnResult030(experience)
        self.enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
        print("Enacted " + str(self.enactedInteraction))
        if self.enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        self.learnCompositeInteraction(self.enactedInteraction)
        self.setEnactedInteraction(self.enactedInteraction)
        return "" + self.getMood()

    def learnCompositeInteraction(self, interaction):
        """
        Learn the composite interaction from the previous enacted interaction and the current enacted interaction
        """
        preInteraction = self.getEnactedInteraction()
        postInteraction = interaction
        #TODO: error here - postInteraction should be None (as in original implementation
        if not(preInteraction is None):
            self.addOrGetCompositeInteraction(preInteraction, postInteraction)

    def addOrGetCompositeInteraction(self, preInteraction, postInteraction):
        """
        Records a composite interaction in memory
        @param preInteraction: The composite interaction's pre-interaction
        @param postInteraction: The composite interaction's post-interaction
        @return the learned composite interaction
        """
        valence = preInteraction.getValence() + postInteraction.getValence()
        interaction = self.addOrGetInteraction(preInteraction.getLabel() + postInteraction.getLabel())
        interaction.setPreInteraction(preInteraction)
        interaction.setPostInteraction(postInteraction)
        interaction.setValence(valence)
        print("learn " + interaction.getLabel())
        return interaction

    def createInteraction(self, label):
        return c_Interaction030(label)

    def anticipate(self):
        """
        Computes the list of anticipations
        @return the list of anticipations
        """
        anticipations = []
        if self.getEnactedInteraction() is not None:
            for activatedInteraction in self.getActivatedInteractions():
                proposedInteraction = activatedInteraction.getPostInteraction()
                new_anticipation = c_Anticipation030(proposedInteraction)
                anticipations += [new_anticipation]
                print("afforded " + str(proposedInteraction))
        return anticipations

    def selectInteraction(self, anticipations):
        anticipations.sort()  #this is why we need __cmp__ and __eq__ in Anticipation030
        if len(anticipations)>0:
            affordedInteraction = anticipations[0].getInteraction()
            if affordedInteraction.getValence() >= 0:
                intendedInteraction = affordedInteraction
            else:
                intendedInteraction = self.getOtherInteraction(affordedInteraction)
        else:
            intendedInteraction = self.getOtherInteraction(None)
        return intendedInteraction

    def getActivatedInteractions(self):
        activatedInteractions = []
        if self.getEnactedInteraction() is not None:
            for activatedInteraction in self.interactions.itervalues():
                if activatedInteraction.getPreInteraction() == self.getEnactedInteraction():
                    activatedInteractions += [activatedInteraction]
        return activatedInteractions

    def getOtherInteraction(self, interaction):
        otherInteraction = self.interactions.values()[0]  #the first one
        if interaction is not None:
            for e in self.interactions.itervalues():
                if (e.getExperience() is not None) and (e.getExperience() != interaction.getExperience()):
                    otherInteraction =  e
                    break
        return otherInteraction

    def setEnactedInteraction(self, enactedInteraction):
        self.enactedInteraction = enactedInteraction

    def getEnactedInteraction(self):
        if hasattr(self, "enactedInteraction"):
            return self.enactedInteraction

    def returnResult030(self, experience):
        """
        Environment030
        Results in R1 when the current experience equals the previous experience
        and in R2 when the current experience differs from the previous experience.
        """
        if self.getPreviousExperience() == experience:
            result = self.createOrGetResult(self.LABEL_R1)
        else:
            result = self.createOrGetResult(self.LABEL_R2)
        self.setPreviousExperience(experience)
        return result







