from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction031 import c_Interaction031
from existence.Existence030 import c_Existence030
from agent.Anticipation031 import c_Anticipation031

class c_Existence031(c_Existence030):
    """
    Existence031 can adapt to Environment010 020 030 031.
    Like Existence030, Existence031 seeks to enact interactions that have positive valence.
    Existence031 illustrates the benefit of reinforcing the weight of composite interactions
    and of using the weight of activated interactions to balance the decision.
    """
    def initExistence(self):
        super(c_Existence031, self).initExistence()  # super(c_Existence031, self) <=> c_Existence030
        self.T1 = 8
        self.T2 = 15
        self.clock = 0

    def step(self):
        anticipations = self.anticipate()
        experience = self.selectExperience(anticipations)
        #Change the call to the function returnResult to change the environment
        #result = self.returnResult010(experience)
        result = self.returnResult030(experience)
        #result = self.returnResult031(experience)
        self.enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
        print("Enacted " + str(self.enactedInteraction))
        if self.enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        self.learnCompositeInteraction(self.enactedInteraction)
        self.setEnactedInteraction(self.enactedInteraction)
        return "" + self.getMood()

    def learnCompositeInteraction(self, enactedInteraction):
        """
        Record the composite interaction from the context interaction and the enacted interaction.
	    Increment its weight.
        """
        preInteraction = self.getEnactedInteraction()
        postInteraction = enactedInteraction
        if preInteraction is not None:
            interaction = self.addOrGetCompositeInteraction(preInteraction, postInteraction)
            interaction.incrementWeight()

    def createInteraction(self, label):
        return c_Interaction031(label)

    def anticipate(self):
        """
        Computes the list of anticipations
	    @return the list of anticipations
        """
        anticipations = self.getDefaultAnticipations()
        if self.getEnactedInteraction() is not None:
            for activatedInteraction in self.getActivatedInteractions():
                an_experience = activatedInteraction.getPostInteraction().getExperience()
                a_proclivity = activatedInteraction.getWeight() * activatedInteraction.getPostInteraction().getValence()
                proposition = c_Anticipation031(an_experience, a_proclivity)
                if proposition in anticipations: #if there are any with the same experience (same object of type Experiment)
                    i = anticipations.index(proposition)
                    anticipations[i].addProclivity(a_proclivity)
                else:
                    anticipations.add(proposition)
        return anticipations

    def getDefaultAnticipations(self):
        # all experiences as proposed by default with a proclivity of 0
        anticipations = []
        for experience in self.experiences.itervalues():
            anticipations += [c_Anticipation031(experience, 0)]
        return anticipations

    def selectExperience(self, anticipations):
        # The list of anticipations is never empty because all the experiences are proposed by default with a proclivity of 0
        anticipations.sort()  #we need max or min?
        for anticipation in anticipations:  #hate the names with only one different symbol..
            print("propose " + str(anticipation))
        selectedAnticipation = anticipations[0]  #sounds inefficient to sort an array to find a max
        return selectedAnticipation.getExperience()

    def incClock(self):
        self.clock += 1

    def getClock(self):
        return self.clock

    def returnResult031(self, experience):
        """
        Environment031
        Before time T1 and after time T2: E1 results in R1; E2 results in R2
        between time T1 and time T2: E1 results R2; E2results in R1.
        """
        self.incClock()
        if (self.getClock() <= self.T1) or (self.getClock() > self.T2): #we have tight timing
            if experience == self.addOrGetExperience(self.LABEL_E1):
                #why not checking labels everywhere?...
                result = self.createOrGetResult(self.LABEL_R1)
            else:
                result = self.createOrGetResult(self.LABEL_R2)
        else:
            if experience == self.addOrGetExperience(self.LABEL_E1):
                result = self.createOrGetResult(self.LABEL_R2)
            else:
                result = self.createOrGetResult(self.LABEL_R1)
        return result

