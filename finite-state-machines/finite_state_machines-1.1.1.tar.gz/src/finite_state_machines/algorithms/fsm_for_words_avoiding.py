"""
    An algorithm class for creating the FSM for avoiding a list of words.
"""

from typing import (
    TYPE_CHECKING,
    Dict,
    Hashable,
    Iterable,
    Iterator,
    List,
    MutableMapping,
    Optional,
    Set,
    Tuple,
)

State = Tuple[str, ...]

if TYPE_CHECKING:
    from finite_state_machines import FiniteStateMachine


class Labeler(MutableMapping[Hashable, int]):
    """
    A helper class that assigns integer labels to things you give it, and returns them
    when you ask.
    """

    def __init__(self) -> None:
        self._labels: Dict[Hashable, int] = dict()

    def __len__(self) -> int:
        return len(self._labels)

    def __iter__(self) -> Iterator[Hashable]:
        return iter(self._labels)

    def __delitem__(self, key: Hashable) -> None:
        del self._labels[key]

    def __getitem__(self, key: Hashable) -> int:
        if key not in self._labels:
            self._labels[key] = len(self._labels)
        return self._labels[key]

    def __setitem__(self, key: Hashable, value: int) -> None:
        raise NotImplementedError


class WordAvoidanceFSM:
    """
    An algorithm class for computing the FSM that accepts all words that avoid
    a given list of bad words. If "alphabet" is not specified in the initializer,
    it is inferred to be the set of letters that appear in some word that must be
    avoided.
    """

    def __init__(
        self, words_to_avoid: Iterable[str], alphabet: Optional[Set[str]] = None
    ) -> None:
        self.words_to_avoid = sorted(words_to_avoid)
        if alphabet is not None:
            self.alphabet = sorted(alphabet)
        else:
            self.alphabet = sorted(
                {letter for word in words_to_avoid for letter in word}
            )

    def machine(self) -> "FiniteStateMachine":
        """
        create the machine that accepts all words avoiding self.words_to_avoid
        """
        from finite_state_machines import FiniteStateMachine  # pylint: disable=C0415

        labeler = Labeler()

        start_state: State = tuple("" for _ in range(len(self.words_to_avoid)))
        transitions: Dict[Tuple[int, str], int] = {}

        states_processed: Set[State] = set()
        states_to_process: List[State] = [start_state]

        while states_to_process:
            state = states_to_process.pop(0)
            states_processed.add(state)
            for letter in self.alphabet:
                next_state = self.next_state(state, letter)
                if any(
                    next_state[i] == self.words_to_avoid[i]
                    for i in range(len(self.words_to_avoid))
                ):
                    transitions[(labeler[state], letter)] = labeler["garbage"]
                else:
                    if next_state not in states_processed:
                        states_to_process.append(next_state)
                    transitions[(labeler[state], letter)] = labeler[next_state]

        for letter in self.alphabet:
            transitions[(labeler["garbage"], letter)] = labeler["garbage"]

        # return some stuff, accepting = everything but garbage?
        accepting = set(labeler.values()).difference({labeler["garbage"]})
        start = labeler[start_state]
        return FiniteStateMachine(
            set(self.alphabet), len(labeler), start, accepting, transitions
        )

    def next_state(self, state: State, letter: str) -> State:
        """
        Computes the next state reached after reading <letter> in state <state>.
        """
        return tuple(
            WordAvoidanceFSM.prefix_made(self.words_to_avoid[i], state[i] + letter)
            for i in range(len(state))
        )

    @staticmethod
    def prefix_made(word_avoiding: str, word_built: str) -> str:
        """
        Computes the largest prefix of <word_avoiding> that <word_built> matches.
        """
        end_index = len(word_avoiding)
        while word_avoiding[:end_index] != word_built[len(word_built) - end_index :]:
            end_index -= 1
        return word_avoiding[:end_index]
