import numpy as np

from pysnakegym.mdp.state import BooleanState, GridState


class MDPAction(object):

    def __init__(self, action: int):
        self.action = action

    def get_action(self):
        pass


class MDP(object):
    """
    A discrete Markov Decision Process (MDP).
    """

    def __init__(self):
        self.environment = None
        self.state_representation = None
        self._reward_sum = 0
        self._n_steps = 0
        self._score = 0

    def reset(self) -> (np.array, float, bool):
        """
        Resets the MDP to its start state.
        :return: a triplet containing the start state, initial reward, and whether the state is final.
        """
        pass

    def step(self, action: np.array) -> (np.array, float, bool):
        """
        Takes a discrete step within the MDP.
        :param action: the action to be taken. The encoding of this is problem dependent
        :return: a triplet containing the new state resulting from the action, the reward obtained from the action,
        and whether the new state is final.
        """
        pass

    def reward_sum(self) -> float:
        """
        Gets the sum of all rewards of this MDP up until and including the previous action.
        :return: the sum of all rewards
        """
        return self._reward_sum

    def n_steps(self) -> int:
        """
        Gets the number of steps of this MDP up until and including the previous action.
        :return: an integer >= 0 that is the number of steps
        """
        return self._n_steps

    def env_score(self) -> float:
        """
        The score that is being tracked inside the environment, for a game of snake this would be the number of apples
        eaten for example
        :return: a float that is the score within the environment
        """
        return self._score

    def state_dims(self) -> (int, int):
        """
        Gets the dimensions of the state as a tuple
        :return: a tuple of two integers.
        """
        pass

    def n_actions(self) -> int:
        """
        Gets the number of actions that the agent can take in each MDP.
        :return: an int
        """
        pass

    def set_state_representation(self, state_representation: str) -> None:
        """
        Sets the state representation that will be used by the MDP. Possible values are 'BOOLEAN' and 'GRID'.
        """
        if state_representation == 'BOOLEAN':
            self.state_representation = BooleanState(self.environment)
        elif state_representation == 'GRID':
            self.state_representation = GridState(self.environment)

