from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction020 import c_Interaction020
from existence.Existence010 import c_Existence010


"""
An Existence020 is a sort of Existence010 in which each Interaction has a predefined Valence.
When a given Experience is performed and a given Result is obtained, the corresponding Interaction is considered enacted.
The Existence020 is PLEASED when the enacted Interaction has a positive or null Valence, and PAINED otherwise.
An Existence020 is still a single entity rather than being split into an explicit Agent and Environment.
An Existence020 demonstrates a rudimentary decisional mechanism and a rudimentary learning mechanism.
It learns to choose the Experience that induces an Interaction that has a positive valence.
Try to change the Valences of interactions and the method giveResult(experience)
and observe that the Existence020 still learns to enact interactions that have positive valences.
"""

class c_Existence020(c_Existence010):
    def initExistence(self):
        e1 = self.addOrGetExperience(self.LABEL_E1)
        e2 = self.addOrGetExperience(self.LABEL_E2)
        r1 = self.createOrGetResult(self.LABEL_R1)
        r2 = self.createOrGetResult(self.LABEL_R2)
        #Change the valence of interactions to change the agent's motivation
        self.addOrGetPrimitiveInteraction(e1, r1, -1)
        self.addOrGetPrimitiveInteraction(e2, r2, 1)
        self.setPreviousExperience(e1)

    def step(self):
        experience = self.getPreviousExperience()
        if self.getMood() == "PAINED":
            experience = self.getOtherExperience(experience)
        result = self.returnResult010(experience)
        enactedInteraction = self.addOrGetPrimitiveInteraction(experience, result, 0)
        if enactedInteraction.getValence() >= 0:
            self.setMood("PLEASED")
        else:
            self.setMood("PAINED")
        self.setPreviousExperience(experience)
        return experience.getLabel() + result.getLabel() + " " + self.getMood()

    def addOrGetPrimitiveInteraction(self, experience, result, valence):
        """
        Create an interaction as a tuple <experience, result>.
        @param experience: The experience.
        @param result: The result.
        @param valence: the interaction's valence
        @return The created interaction
        """
        label = experience.getLabel() + result.getLabel()
        if not(self.interactions.has_key(label)):
            interaction = self.createInteraction(label)
            interaction.setExperience(experience)
            interaction.setResult(result)
            interaction.setValence(valence)
            self.interactions[label] = interaction
        interaction = self.interactions[label]
        return interaction

    def createInteraction(self, label):
        return c_Interaction020(label)