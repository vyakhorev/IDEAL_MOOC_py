from shared import *

# Implementation of basic actions - physical part
# Action is experience + implementation of it

class c_action(hashable):

    def __init__(self, an_agent):
        self.agent = an_agent
        self.init_setting()

    def __repr__(self):
        return self.label

    def init_setting(self):
        self.timing = 0
        self.label = "act[abstract]"

    def doit(self):
        pass

class c_sword_strike(c_action):

    def init_setting(self):
        self.timing = 5
        self.label = "act[sword strike]"

    def doit(self):
        if self.agent.active_target is None:
            return "missed"
        self.agent.active_target.hitpoints -= 17
        if self.agent.active_target.hitpoints < 0:
            self.agent.active_target.gameover()
        return "hit"

class c_throw_fireball(c_action):

    def init_setting(self):
        self.timing = 7
        self.label = "act[throw fireball]"

    def doit(self):
        if self.agent.active_target is None:
            return "missed"
        self.agent.active_target.hitpoints -= 25
        if self.agent.active_target.hitpoints <= 0:
            self.agent.active_target.gameover()
        return "hit"

class c_cast_heal(c_action):

    def init_setting(self):
        self.timing = 10
        self.label = "act[heal]"

    def doit(self):
        self.agent.hitpoints = min([40+self.agent.hitpoints, 100])
        return "healed"

class c_select_enemy_as_target(c_action):
    def init_setting(self):
        self.timing = 1
        self.label = "act[select enemy]"

    def doit(self):
        #there are 2 agents, so the enemy is the other one
        target_list = self.agent.devs.agents_list
        for trg_i in target_list:
            if trg_i.agent_name <> self.agent.agent_name:
                self.agent.active_target = trg_i
                return "found"
        return "not_found"

class c_select_self_as_target(c_action):
    def init_setting(self):
        self.timing = 0
        self.label = "act[select self]"

    def doit(self):
        self.agent.active_target = self.agent
        return "found"
