from coupling.Experiment import c_Experiment
from coupling.Result import c_Result
from coupling.Interaction010 import c_Interaction010
from existence.Existence import c_Existence

"""
An c_Existence010 simulates a "stream of intelligence" made of a succession of Experiences and Results.
The c_Existence010 is SELF-SATISFIED when the c_Result corresponds to the c_Result it expected, and FRUSTRATED otherwise.
Additionally, the Existence0 is BORED when it has been SELF-SATISFIED for too long, which causes it to try another Experience.
An Existence1 is still a single entity rather than being split into an explicit Agent and Environment.
"""

class c_Existence010(c_Existence):
    LABEL_E1 = "e1"
    LABEL_E2 = "e2"
    LABEL_R1 = "r1"
    LABEL_R2 = "r2"
    BOREDOME_LEVEL = 4

    def __init__(self):
        self.mood = "BORED"  #Just using strings like "SELF_SATISFIED", "FRUSTRATED", "BORED", "PAINED", "PLEASED"
        self.interactions = dict()
        self.results = dict()
        self.experiences = dict()
        self.initExistence()


    def initExistence(self):
        e1 = self.addOrGetExperience(self.LABEL_E1)
        self.addOrGetExperience(self.LABEL_E2)
        self.setPreviousExperience(e1)

    def step(self):
        experience = self.getPreviousExperience()
        if self.getMood() == "BORED":
            experience = self.getOtherExperience(experience)
            self.setSatisfactionCounter(0)
        anticipated_result = self.predict(experience)
        result = self.returnResult010(experience)
        self.addOrGetPrimitiveInteraction(experience, result)
        if result == anticipated_result:
            self.setMood("SELF_SATISFIED")
            self.incSatisfactionCounter()
        else:
            self.setMood("FRUSTRATED")
            self.setSatisfactionCounter(0)
        if self.getSatisfactionCounter() >= self.BOREDOME_LEVEL:
            self.setMood("BORED")
        self.setPreviousExperience(experience)
        return experience.getLabel() + result.getLabel() + " " + str(self.getMood())

    def addOrGetPrimitiveInteraction(self, an_experience, a_result):
        """
        * Create an interaction as a "tuple" <experience, result>.
        * @param experience: The experience.
        * @param result: The result.
        * @return The created interaction
        """
        interaction = self.addOrGetInteraction(an_experience.getLabel() + a_result.getLabel())
        interaction.setExperience(an_experience)
        interaction.setResult(a_result)
        return interaction

    def addOrGetInteraction(self, label):
        """
        * Records an interaction in memory.
        * @param label: The label of this interaction.
        * @return The interaction.
        """
        if not(self.interactions.has_key(label)):
            self.interactions[label] = self.createInteraction(label)
        return self.interactions[label]


    def createInteraction(self, label):
        new_interaction = c_Interaction010(label)
        return new_interaction

    def getInteraction(self, label):
        """
        * Finds an interaction from its label
        * @param label: The label of this interaction.
        * @return The interaction.
        """
        if self.interactions.has_key(label):
            return self.interactions[label]

    def predict(self, experience):
        """
        Finds an interaction from its experience
        @return The interaction.
        """
        chosen_key = None
        anticipated_result = None
        for k_i, interaction_i in self.interactions.iteritems():
            if interaction_i.getExperience() == experience:
                chosen_key = k_i  #could original Java code destroy interactions with same experience?...
        if chosen_key:
            anticipated_result = self.interactions[chosen_key].getResult()
        return anticipated_result

    def addOrGetExperience(self, label):
        """
        Creates a new experience from its label and stores it in memory.
        @param label: The experience's label
        @return The experience.
        """
        if not(self.experiences.has_key(label)):
            self.experiences[label] = self.createExperience(label)
        return self.experiences[label]

    def createExperience(self, label):
        return c_Experiment(label)

    def getOtherExperience(self, an_experience):
        """
        Finds an experience different from that passed in parameter.
        @param experience: The experience that we don't want
        @return The other experience.
         """
        other_experience = None
        for exp in self.experiences.itervalues():
            if exp != an_experience:
                other_experience = exp
                break
        return other_experience

    def createOrGetResult(self, label):
        """
        Creates a new result from its label and stores it in memory.
        @param label: The result's label
        @return The result.
        """
        if not(self.results.has_key(label)):
            self.results[label] = c_Result(label)  #hey, why not "createResult"?  :-)
        return self.results[label]

    def getMood(self):
        return self.mood

    def setMood(self, a_mood):
        self.mood = a_mood

    def getPreviousExperience(self):
        if hasattr(self, "previous_experience"):
            return self.previous_experience

    def setPreviousExperience(self, an_experience):
        self.previous_experience = an_experience

    def getSatisfactionCounter(self):
        return self.satisfaction_counter

    def setSatisfactionCounter(self, sat_count):
        self.satisfaction_counter = sat_count

    def incSatisfactionCounter(self):
        self.satisfaction_counter += 1

    def returnResult010(self, an_experience):
        """
        The Environment010
        E1 results in R1. E2 results in R2.
        @param experience: The current experience.
        @return The result of this experience.
        """
        if an_experience == self.addOrGetExperience(self.LABEL_E1):
            return self.createOrGetResult(self.LABEL_R1)
        else:
            return self.createOrGetResult(self.LABEL_R2)








