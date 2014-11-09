import simpy
import dev_agent
import environment

"""
#IDEALMOOC034 - programming activity
The agent can do primitive actions:
1) attack
2) heal
3) select opponent
4) select self

Each action, being enacted, returns a predefined tuple (result, valence).
Result is just a string. Valence is aggressive - positive for attacking opponent, negative for attacking self,
positive for healing self, negative for healing the opponent.

A result should look like the agent remembers composite interactions and stop attacking himself and healing opponent.

"""

agent_E = dev_agent.c_swordsman("Mighty Ernest")
agent_V = dev_agent.c_magician("Wizard Vasya")

# First one is fast, second one is real-time (factor = 0.1 means that each time unit in the code takes 1/10 seconds to run).
env = simpy.Environment()
#env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=0.1, strict=True)

the_devs = environment.c_devs_environment(env)
the_devs.set_seed(12345)  # remove the number to turn it random
the_devs.add_agent(agent_E)
the_devs.add_agent(agent_V)
the_devs.prepare_for_simulation()
the_devs.simpy_env.process(the_devs.my_generator())
the_devs.simpy_env.run(until = 150)
