from shared import *
from interaction import *

class c_dev_agent(object):
    #Agent is existance
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.init_setting()
        self.actions = dict() # given from environment
        #self.results = dict() # to learn
        self.primitive_interactions = dict()
        self.complex_interactions = dict()
        self.last_enacted_intercation = None
        self.previously_enacted_interaction = None
        self.received_valence = 0
        self.actual_result = ""
        self.chosen_action = None
        self.feelings = "NOTHING"
        self.defeated = 0

    def __repr__(self):
        return self.agent_name

    def init_setting(self):
        pass

    def log_repr(self):
        return self.agent_name

    def step(self):
		# The intercation cycle. Agent can no longer quit the game with "GAMEOVER".
		# Instead, he could be knocked down for long. This is done to keep its memory.
        while 1:
            self.devs.sent_log(self, "my hp:" + str(self.hitpoints))
            self.chosen_action = self.do_select_action()
            self.devs.sent_log(self, "enact: " + str(self.chosen_action))
            yield self.devs.simpy_env.process(self.devs.run_action(self.chosen_action))
            self.devs.sent_log(self, "result: " + str(self.actual_result))
            self.do_introspect()


    def do_select_action(self):
        # We anticipate al list of interactions based on last enacted interaction (self.enacted_intercation)
        # Then we choose one with maximum valence. Mood no longer governs our selection policy.
        # However, as we select a maximum valence interaction, we try to approach a "PLEASED" feeling.

        # 1 Anticipate based on enacted_intercation
        anticipations = []
        if self.previously_enacted_interaction is not None:
            for int_i in self.complex_interactions.values():
                if int_i.pre_interaction == self.previously_enacted_interaction:
                    anticipations += [int_i.post_interaction]  #this would be primitive interaction
        self.devs.sent_log(self, "...context " + str(self.previously_enacted_interaction))
        self.devs.sent_log(self, "...anticipate primitive interactions " + str(anticipations))

        # 2 Select an action that matches to the anticipation with highest valence
        # In anticipations we have only primitive interactions with given valence.
        # We do not check valence of complex interactions yet .
        max_valence = 0
        best_action = None
        for int_i in anticipations:
            if int_i.valence > max_valence:
                best_action = int_i.experience
                max_valence = int_i.valence
        if best_action is None: # no solution found - panic and pick random
            best_action = self.devs.random_generator.choice(self.actions.values())
        return best_action

    def do_introspect(self):
        # While introspecting, we
        # 1 Record or get primitive interacion
        # 2 Record new complex interaction
        # So in self.interactions we have both primitive and complex interactions
        # The most complex interaction consists only of a tuple.

        # 1 Find a primitive interaction that was acually enacted
        k = str((self.chosen_action, self.actual_result))
        if self.primitive_interactions.has_key(k):
            self.last_enacted_intercation = self.primitive_interactions[k]
        else: #first time
            new_primitive_interaction = c_intercation(k)
            new_primitive_interaction.experience = self.chosen_action
            new_primitive_interaction.result = self.actual_result
            new_primitive_interaction.valence = self.received_valence
            self.primitive_interactions[k] = new_primitive_interaction
            self.last_enacted_intercation = new_primitive_interaction
            self.devs.sent_log(self, "...learned a primitive interaction " + str(new_primitive_interaction))

        # 2 Remember complex interaction within this context.
        if self.previously_enacted_interaction is not None and self.last_enacted_intercation is not None:
            k = str((self.previously_enacted_interaction, self.last_enacted_intercation))
            if not(self.complex_interactions.has_key(k)):
                # First time this combo is enacted
                new_complex_interaction = c_intercation(k)
                new_complex_interaction.pre_interaction = self.previously_enacted_interaction
                new_complex_interaction.post_interaction = self.last_enacted_intercation
                self.complex_interactions[k] = new_complex_interaction
                self.devs.sent_log(self, "...learned a complex interaction " + str(new_complex_interaction))

        # Last enacted is now the context
        self.previously_enacted_interaction = self.last_enacted_intercation
        self.update_feelings()

    def update_feelings(self):
        # Feelings is just an indicator, not a decisional mechanism
        if self.received_valence >= 0:
            self.feelings = "PLEASED"
        else:
            self.feelings = "PAINED"
        self.devs.sent_log(self, "i feel " + self.feelings)


    def add_available_action(self, new_action):
        # This is part of the setting: a swordsman cannot throw fireballs, magician does not have a sword.
        # This is decided in the environment.
        self.actions[new_action.key()] = new_action

class c_swordsman(c_dev_agent):
    def init_setting(self):
        self.hitpoints = 100
        self.active_target = None

    def dnd_classes(self):
        return ["fighter"]

    def gameover(self):
        # game over - not a complete end
        self.devs.sent_log(self, "defeated")
        self.revive() #revive instantly

    def revive(self):
        self.hitpoints = 100
        self.devs.sent_log(self, "revived")

class c_magician(c_dev_agent):
    def init_setting(self):
        self.hitpoints = 100
        self.active_target = None

    def dnd_classes(self):
        return ["wizard"]

    def gameover(self):
        # game over - not a complete end
        self.devs.sent_log(self, "defeated")
        self.revive() #revive instantly

    def revive(self):
        self.hitpoints = 100
        self.devs.sent_log(self, "revived")












