import random as mrandom #Imported as mrandom to prevent conflicts

from .exception import *

gen = mrandom.SystemRandom()

class rand:
    """Random class"""
    def randint(self, s, e):
        """Generates a (maybe) cryptographically secure number using random.SystemRandom.randint()"""
        global gen
        return gen.randint(s, e)

    def srandint(self, seed, s, e):
        """Generates a seeded randint like above.
        Note, this function is not cryptographically secure because of the fact
        that it has to be seeded, If you would
        like it to be secure, use beetroot.random.randint() instead."""
        mrandom.seed(seed)
        return mrandom.randint(s, e)

random = rand()
del rand