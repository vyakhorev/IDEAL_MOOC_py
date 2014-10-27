from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction032 import c_Interaction032
from existence.Existence032 import c_Existence032
from agent.Anticipation032 import c_Anticipation032
from tracer.Trace import c_Trace

class c_Existence033(c_Existence032):
    """
    Like Existence030, Existence032 can adapt to Environment010, Environment020, and Environment030.
    Again, it is PLEASED when the enacted Interaction has a positive or null Valence, and PAINED otherwise.
    Additionally, like Existence010, Existence032 is SELF-SATISFIED when it correctly anticipated the result, and FRUSTRATED otherwise.
    It is also BORED when it has been SELF-SATISFIED for too long.
    Try to change the Valences of interactions and the reality defined in Existence2.initExistence(),
    and observe that Existence032 tries to balance satisfaction and pleasure.
    (when the valence of interaction are all set to 0, then only satisfaction/frustration/boredom drives Existence032's choices)
    Existence032 illustrates the benefit of implementing different motivational dimensions.
    """
    def step(self):
        anticipations = self.anticipate()
        intendedInteraction = self.selectInteraction(anticipations)
        experience = intendedInteraction.getExperience()
        # Change the call to the function returnResult to change the environment
        #result = self.returnResult010(experience)
        #result = self.returnResult030(experience)
        result = self.returnResult031(experience)
        enactedInteraction = self.getInteraction(experience.getLabel() + result.getLabel())
        print("Enacted "+ str(enactedInteraction))
        if enactedInteraction <> intendedInteraction:
            intendedInteraction.addAlternateInteraction(enactedInteraction)
            print("Alternate "+ enactedInteraction.getLabel())
        if enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        if enactedInteraction == intendedInteraction:
            self.setMood("SELF_SATISFIED")
            self.incSatisfactionCounter()
        else:
            self.setMood("FRUSTRATED")
            self.setSatisfactionCounter(0)
        self.learnCompositeInteraction(enactedInteraction)
        self.setEnactedInteraction(enactedInteraction)
        return self.getMood()

    def selectInteraction(self, anticipations):
        """* Compute the system's mood and
	    and choose the next experience based on the previous interaction
	    @return The next experience. """
        anticipations.sort()
        intendedInteraction = self.getOtherInteraction(None)
        if self.getSatisfactionCounter() < self.BOREDOME_LEVEL:
            if len(anticipations) > 0:
                proposedInteraction = anticipations[0].getInteraction()
                if proposedInteraction.getValence() >= 0:
                    intendedInteraction = proposedInteraction
                else:
                    intendedInteraction = self.getOtherInteraction(proposedInteraction)
        else:
            self.setSatisfactionCounter(0)
            if len(anticipations) == 1:
                intendedInteraction = self.getOtherInteraction(anticipations[0].getInteraction())
            elif len(anticipations) > 1:
                #What's the big difference between 0 and 1 ?
                intendedInteraction = anticipations[1].getInteraction()
        return intendedInteraction