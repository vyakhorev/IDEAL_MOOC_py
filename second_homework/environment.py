from shared import *
from actions import *

class c_devs_environment(object):
    def __init__(self, simpy_env):
        self.simpy_env = simpy_env
        self.random_generator = None
        self.agents_list = []
        self.init_setting()
        self.possible_actions = c_action.__subclasses__()

    def log_repr(self):
        return "the_system"

    def nowsimtime(self):
        return self.simpy_env.now

    def add_agent(self, new_agent):
        new_agent.devs = self
        self.afford_actions_to_agent(new_agent)
        self.agents_list += [new_agent]

    def afford_actions_to_agent(self, agent):
        for cl_i in agent.dnd_classes():
            if cl_i == "fighter":
                agent.add_available_action(c_sword_strike(agent))
            if cl_i == "wizard":
                agent.add_available_action(c_throw_fireball(agent))
            agent.add_available_action(c_select_opponent_as_target(agent))
            agent.add_available_action(c_select_self_as_target(agent))
            agent.add_available_action(c_cast_heal(agent))

    def set_seed(self, seed = None):
        if seed is None:
            seed = random.randint(0, sys.maxint)
        self.random_generator = random.Random(seed)

    def my_generator(self):
        for ag_i in self.agents_list:
            self.simpy_env.process(ag_i.step())
        yield empty_event(self.simpy_env) #Formality

    def sent_log(self, sender_instance, msg_text, msg_priority = 1):
        sender_name = sender_instance.log_repr()  #make this readable in any class
        timestamp = self.nowsimtime()
        print("@[%d] #[%s] : %s"% (timestamp, sender_name, msg_text))

    def run_action(self, an_action):
        # valence is given with actions results. So it is preset with primitive interactions
        yield self.simpy_env.timeout(an_action.timing) # wait till the action is done
        (action_result, a_valence) = an_action.doit()
        an_action.agent.actual_result = action_result
        an_action.agent.received_valence = a_valence

    def init_setting(self):
        pass

    def prepare_for_simulation(self):
        # enact self targeting - agent can switch targets later.
        # this done before timer starts to tick.
        for agent in self.agents_list:
            an_action = c_select_self_as_target(agent)
            an_action.doit()