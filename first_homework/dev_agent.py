from shared import *
from interaction import *

class c_dev_agent(object):
    #Agent is existance
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.init_setting()
        self.primitive_actions = dict() # preset
        self.actions= dict() # to learn
        self.results = dict() # to learn
        self.interactions = dict()  # to learn
        self.valences = dict()  # to learn
        self.sat_counter = 0
        self.boredome_level = 3
        self.previous_action = None
        self.mood = ""
        self.alive = 1
        self.feelings = ""

    def __repr__(self):
        return self.agent_name

    def init_setting(self):
        pass

    def log_repr(self):
        return self.agent_name

    def step(self):
		# The intercation cycle
        while self.alive:
            self.devs.sent_log(self, "my hp:" + str(self.hitpoints))
            self.chosen_action = self.do_select_action()
			# the code will wait till the process below finishes
            # "run_action" of environment would change the agent
            yield self.devs.simpy_env.process(self.devs.run_action(self.chosen_action))
            self.devs.sent_log(self, "result " + str(self.actual_result))
            self.do_introspect()
            self.previous_action = self.chosen_action

    def do_select_action(self):
        # selects or generates an "experiment"
        if self.mood == "BORED" or self.feelings == "PAINED" or self.previous_action is None:
            # another action
            filtered_actions = []
            for act_i in self.primitive_actions.values():
                if act_i <> self.previous_action:
                    filtered_actions += [act_i]
            the_action = self.devs.random_generator.choice(filtered_actions)
        else:
            the_action = self.previous_action
        self.anticipated_result = self.predict_result(the_action)
        self.devs.sent_log(self, "enact " + str(the_action)+"" + " expect " + str(self.anticipated_result))
        return the_action

    def do_introspect(self):
        # Anticipations
        if self.anticipated_result == self.actual_result:
            self.mood = "SATISFIED"
            self.sat_counter += 1
        else:
            self.mood = "FRUSTRATED"
            self.sat_counter = 0
        if self.sat_counter >= self.boredome_level:
            self.mood = "BORED"
            self.sat_counter = 0
        self.devs.sent_log(self, "my mood is " + self.mood)
        # Remember interaction
        self.memorize_interaction(self.chosen_action, self.actual_result)
        # Remember recieved valence. Since we may have unstationary environment, we'll adjust it
        k = (self.chosen_action, self.actual_result)
        if self.valences.has_key(k):
            self.valences[k] = self.received_valence * 0.5 + self.valences[k] * 0.5
        else:
            self.valences[k] = self.received_valence
        if self.valences[k] >= 0:
            self.feelings = "PLEASED"
        else:
            self.feelings = "PAINED"
        self.devs.sent_log(self, "i feel " + self.feelings)

    def predict_result(self, an_action):
        # gives deterministic prediction
        chosen_key = None
        anticipated_result = None
        for k_i, interaction_i in self.interactions.iteritems():
            if interaction_i.get_experience() == an_action:  # checks action.label
                chosen_key = k_i
        if chosen_key is not None:
            anticipated_result = self.interactions[chosen_key].get_result()
        return anticipated_result

    def add_available_action(self, new_action):
        # This is part of the setting: a swordsman cannot throw fireballs, magician does not have a sword.
        # This is decided in the environment.
        self.primitive_actions[new_action.key()] = new_action

    def memorize_interaction(self, enacted_action, actual_result):
        key_for_int = (enacted_action, actual_result)
        if not(self.interactions.has_key(key_for_int)):
            an_int = c_intercation(key_for_int)
            an_int.set_experience(enacted_action)
            an_int.set_result(actual_result)
            self.interactions[an_int.key()] = an_int

class c_swordsman(c_dev_agent):
    def init_setting(self):
        self.hitpoints = 100
        self.active_target = None

    def dnd_classes(self):
        return ["fighter"]

    def gameover(self):
        # game over
        self.devs.sent_log(self, "GAMEOVER")
        self.alive = 0

class c_magician(c_dev_agent):
    def init_setting(self):
        self.hitpoints = 100
        self.active_target = None

    def dnd_classes(self):
        return ["wizard"]

    def gameover(self):
        # game over
        self.devs.sent_log(self, "GAMEOVER")
        self.alive = 0










