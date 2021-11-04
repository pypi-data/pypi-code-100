from engine.devices import RL


def create_syst(abc):
    abc = abc * 2
    d = RL.create(3)
    x = d * abc

    return x
