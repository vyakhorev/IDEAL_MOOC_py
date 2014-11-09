from shared import *

# Implementation of basic actions. Action is experience + implementation of it.
# With "doit" returns a tuple (result, valence). Result is just a string.

class c_action(hashable):

    def __init__(self, an_agent):
        self.agent = an_agent
        self.init_setting()

    def __repr__(self):
        return self.label

    def init_setting(self):
        self.timing = 0
        self.label = "[abstract]"

    def doit(self):
        #TODO: yield and run explicit process here
        #to do that, we may send (result, valence) tuple to the agent and yield other events to the environment
        # returns (result, valence)
        return ("[nothing]", 0)

class c_sword_strike(c_action):

    def init_setting(self):
        self.timing = 5
        self.label = "[sword strike]"

    def doit(self):
        self.agent.active_target.hitpoints -= 17
        if self.agent.active_target == self.agent: #hit himself
            return ("[it hurts]", -2)
        if self.agent.active_target.hitpoints < 0:
            self.agent.active_target.gameover()
            return ("[won]", 2)
        return ("[hit opponent]", 1)

class c_throw_fireball(c_action):

    def init_setting(self):
        self.timing = 7
        self.label = "[throw fireball]"

    def doit(self):
        self.agent.active_target.hitpoints -= 25
        if self.agent.active_target == self.agent: #hit himself
            return ("[it hurts]", -2)
        if self.agent.active_target.hitpoints <= 0:
            self.agent.active_target.gameover()
            return ("[won]", 2)
        return ("[hit opponent]", 1)

class c_cast_heal(c_action):

    def init_setting(self):
        self.timing = 10
        self.label = "[heal]"

    def doit(self):
        #heals the active target
        heal_power = 40
        hp_0 = self.agent.active_target.hitpoints
        self.agent.active_target.hitpoints = min([heal_power + hp_0, 100])
        if self.agent.active_target == self.agent:  # agent heals himself
            return ("[healed self]", 1)
        else:  # agent heals opponent
            return ("[healed opponent]", -1)

class c_select_opponent_as_target(c_action):
    def init_setting(self):
        self.timing = 1
        self.label = "[select opponent]"

    def doit(self):
        #there are 2 agents, so the enemy is the other one
        target_list = self.agent.devs.agents_list
        for trg_i in target_list:
            if trg_i.agent_name <> self.agent.agent_name:
                self.agent.active_target = trg_i
                return ("[targeting opponent]", 0)
        return ("[opponent not found]", 0)

class c_select_self_as_target(c_action):
    def init_setting(self):
        self.timing = 0
        self.label = "[select self]"

    def doit(self):
        self.agent.active_target = self.agent
        return ("[targeting self]",0)
