from coupling.Experiment040 import c_Experiment040
from coupling.Interaction032 import c_Interaction032
from existence.Existence032 import c_Existence031
from agent.Anticipation031 import c_Anticipation031


class c_Existence040(c_Existence031):
    #Existence040 implements two-step self-programming.
    def initExistence(self):
        e1 = self.addOrGetExperience(self.LABEL_E1)
        e2 = self.addOrGetExperience(self.LABEL_E2)
        r1 = self.addOrGetExperience(self.LABEL_R1)
        r2 = self.addOrGetExperience(self.LABEL_R2)
        #Change the valence depending on the environment to obtain better behaviors
        e11 = self.addOrGetPrimitiveInteraction(e1, r1, -1)
        e12 = self.addOrGetPrimitiveInteraction(e1, r2, 1) # Use valence 1 for Environment040 and 2 for Environment041
        e21 = self.addOrGetPrimitiveInteraction(e2, r1, -1)
        e22 = self.addOrGetPrimitiveInteraction(e2, r2, 1) # Use valence 1 for Environment040 and 2 for Environment041
        e1.setIntendedInteraction(e12)
        e1.resetAbstract()
        e2.setIntendedInteraction(e22)
        e2.resetAbstract()

    def step(self):
        anticipations = self.anticipate()
        experience = self.selectExperience(anticipations)
        intendedInteraction = experience.getIntendedInteraction()
        print("Inteded " + str(intendedInteraction))
        enactedInteraction = self.enact(intendedInteraction)
        print("Enacted " + str(enactedInteraction))
        if enactedInteraction != intendedInteraction and experience.isAbstract:
            failResult = self.createOrGetResult(enactedInteraction.getLabel().replace('e','E').replace('r','R' + ">"))
            valence = enactedInteraction.getValence()
            enactedInteraction = self.addOrGetPrimitiveInteraction(experience, failResult, valence)
        if enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        self.learnCompositeInteraction(enactedInteraction)
        self.setPreviousSuperInteraction(self.getLastSuperInteraction())
        self.setEnactedInteraction(enactedInteraction)
        return self.getMood()

    def learnCompositeInteraction(self, enactedIntearction):
        """
        Learn composite interactions from
        the previous super interaction, the context interaction, and the enacted interaction
        """
        previousInteraction = self.getEnactedInteraction()
        lastInteraction = enactedIntearction
        previousSuperInteraction = self.getPreviousSuperInteraction()
        lastSuperIntearction = None
        # learn [previous current] called the super interaction
        if previousInteraction is not None:
            lastSuperIntearction = self.addOrGetAndReinforceCompositeInteraction(previousInteraction, lastInteraction)
        # Learn higher-level interactions
        if previousSuperInteraction is not None:
            #and previousInteraction.isPrimitive() and lastInteraction.isPrimitive()
            # learn [penultimate [previous current]]
            self.addOrGetAndReinforceCompositeInteraction(previousSuperInteraction.getPreInteraction(), lastSuperIntearction)
            # learn [[penultimate previous] current]
            self.addOrGetAndReinforceCompositeInteraction(previousSuperInteraction, lastInteraction)
        self.setLastSuperInteraction(lastSuperIntearction)

    def addOrGetAndReinforceCompositeInteraction(self, preInteraction, postInteraction):
        compositeInteraction = self.addOrGetCompositeInteraction(preInteraction, postInteraction)
        compositeInteraction.incrementWeight()  #This is implemented in c_Interaction031
        if compositeInteraction.getWeight() == 1:
            print("learn " + str(compositeInteraction))
        else:
            print("reinforce " + str(compositeInteraction))
        return compositeInteraction

    def addOrGetCompositeInteraction(self, preInteraction, postInteraction):
        """
        Records or get a composite interaction in memory
        If a new composite interaction is created, then a new abstract experience is also created and associated to it.
        @param preInteraction: The composite interaction's pre-interaction
        @param postInteraction: The composite interaction's post-interaction
        @return the learned composite interaction
        """
        label = "<" + str(preInteraction) + str(postInteraction) + ">"
        interaction = self.getInteraction(label)
        if interaction is None:
            interaction = self.addOrGetInteraction(label)
            interaction.setPreInteraction(preInteraction)
            interaction.setPostInteraction(postInteraction)
            interaction.setValence(preInteraction.getValence() + postInteraction.getValence())
            self.addOrGetAbstractExperience(interaction)
            # interaction.setExperience(abstractExperience)
        return interaction

    def addOrGetAbstractExperience(self, interaction):
        label = interaction.getLabel().replace('e', 'E').replace('r', 'R').replace('>', '|')
        if not(self.experiences.has_key(label)):
            abstractExperience = c_Experiment040(label)
            abstractExperience.setIntendedInteraction(interaction)
            interaction.setExperience(abstractExperience)
            self.experiences[label] = abstractExperience
        return self.experiences[label]

    def createInteraction(self, label):
        return c_Interaction032(label)

    def getActivatedInteractions(self):
        contextInteractions = []
        if self.getEnactedInteraction() is not None:
            contextInteractions += [self.getEnactedInteraction().getPostInteraction()]
        if self.getLastSuperInteraction() is not None:
            contextInteractions += [self.getLastSuperInteraction()]
        activatedInteractions = []
        for interaction in self.interactions.itervalues():
            activatedInteraction = interaction
            if not(activatedInteraction.isPrimitive()):
                if activatedInteraction.getPreInteraction() in contextInteractions:
                    activatedInteractions += [activatedInteraction]
                    print("activated " + str(activatedInteraction))
        return activatedInteractions

    def getDefaultAnticipations(self):
        anticipations = []
        for experience in self.experiences.itervalues():
            defaultExperience = experience
            if not(defaultExperience.isAbstract):
                anticipation = c_Anticipation031(experience, 0)
                anticipations += [anticipation]
        return anticipations

    def enact(self, intendedInteraction):
        # receives c_Interaction030, returns Interaction040 ... TODO: understand the point of this
        if intendedInteraction.isPrimitive():
            # We intend to do a single action
            return self.enactPrimitiveIntearction(intendedInteraction)
        else:
            # We intend to try to act a combo
            # Enact the pre-interaction
            enactedPreInteraction = self.enact(intendedInteraction.getPreInteraction())
            if not(enactedPreInteraction == intendedInteraction.getPreInteraction()):
                # if the preInteraction failed then the enaction of the intendedInteraction is interrupted here.
                return enactedPreInteraction
            else:
                # Enact the post-interaction
                enactedPostInteraction = self.enact(intendedInteraction.getPostInteraction())
                return self.addOrGetCompositeInteraction(enactedPreInteraction, enactedPostInteraction)

    def enactPrimitiveIntearction(self, intendedPrimitiveInteraction):
        """
        Implements the cognitive coupling between the agent and the environment
        @param intendedPrimitiveInteraction: The intended primitive interaction to try to enact against the environment
        @param The actually enacted primitive interaction.
        """
        experience = intendedPrimitiveInteraction.getExperience()
        # Change the returnResult() to change the environment
        # Change the valence of primitive interactions to obtain better behaviors
        #result = self.returnResult010(experience)
        #result = self.returnResult030(experience)
        #result = self.returnResult031(experience)
        result = self.returnResult040(experience)
        #result = self.returnResult041(experience)
        return self.addOrGetPrimitiveInteractionSimple(experience, result)

    def addOrGetPrimitiveInteractionSimple(self, an_experience, a_result):
        # In Java code this one is called from c_Existence010 parent.
        interaction = self.addOrGetInteraction(an_experience.getLabel() + a_result.getLabel())
        interaction.setExperience(an_experience)
        interaction.setResult(a_result)
        return interaction

    def createExperience(self, label):
        return c_Experiment040(label)

    def getPreviousSuperInteraction(self):
        if hasattr(self, "previousSuperInteraction"):
            return self.previousSuperInteraction

    def setPreviousSuperInteraction(self, previousSuperInteraction):
        self.previousSuperInteraction = previousSuperInteraction

    def getLastSuperInteraction(self):
        if hasattr(self, "lastSuperInteraction"):
            return self.lastSuperInteraction

    def setLastSuperInteraction(self, lastSuperInteraction):
        self.lastSuperInteraction = lastSuperInteraction

    """
    Environment040
    Results in R2 when the current experience equals the previous experience and differs from the penultimate experience.
    and in R1 otherwise.
    e1->r1 e1->r2 e2->r1 e2->r2 etc.
    """

    def setPenultimateExperience(self, penultimateExperience):
        self.penultimateExperience = penultimateExperience

    def getPenultimateExperience(self):
        if hasattr(self, "penultimateExperience"):
            return self.penultimateExperience

    def returnResult040(self, experience):
        result = self.createOrGetResult(self.LABEL_R1)
        if hasattr(self, "penultimateExperience"):  #just to prevent miss-call
            if self.getPenultimateExperience() != experience and self.getPreviousExperience() == experience:
                result = self.createOrGetResult(self.LABEL_R2)
        self.setPenultimateExperience(self.getPreviousExperience())
        self.setPreviousExperience(experience)
        return result

    """
    Environment041
    The agent must alternate experiences e1 and e2 every third cycle to get one r2 result the third time:
    e1->r1 e1->r1 e1->r2 e2->r1 e2->r1 e2->r2 etc.
    """

    def setAntePenultimateExperience(self, antepenultimateExperience):
        self.antepenultimateExperience = antepenultimateExperience

    def getAntePenultimateExperience(self):
        if hasattr(self, "antepenultimateExperience"):
            return self.antepenultimateExperience

    def returnResult041(self, experience):
        result = self.createOrGetResult(self.LABEL_R1)
        if hasattr(self, "antepenultimateExperience") and hasattr(self, "penultimateExperience"):  #just to prevent miss-call with the 1st run
            if self.getAntePenultimateExperience() != experience and self.getPenultimateExperience() == experience and self.getPreviousExperience() == experience:
                result = self.createOrGetResult(self.LABEL_R2)
        self.setAntePenultimateExperience(self.getPenultimateExperience())
        self.setPenultimateExperience(self.getPreviousExperience())
        self.setPreviousExperience(experience)
        return result




