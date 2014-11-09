import random
import sys

class hashable(object):
    def key(self):
        return self.label

    def __hash__(self):
        return hash(self.key())

    def __eq__(x, y):
        if (y is not None) and (x is not None):
            return x.key() == y.key()


def empty_event(simpy_env):
	return simpy_env.timeout(0)

