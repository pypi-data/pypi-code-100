"""Extraction of common methods for class that contains a set of cards"""
from typing import Iterable, Iterator, Any

from whist.core.cards.card import Card


class CardContainer:
    """
    Super class for all class containing unordered cards.
    """

    def __init__(self, *args: (tuple[Iterable[Card]], tuple[Card, ...])) -> None:
        """
        Constructor

        :param args: multiple cards or one card iterable
        """
        if len(args) == 1 and not isinstance(args[0], Card):
            self._cards = {*args[0]}
        else:
            self._cards = {*args}

    def __contains__(self, card: Card) -> bool:
        return card in self._cards

    def __len__(self):
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards)

    def __str__(self) -> str:
        return str(self._cards)

    def __repr__(self) -> str:
        return f'CardContainer(cards={self._cards!r})'

    def __eq__(self, other: Any) -> bool:
        if self.__class__ is other.__class__:
            # pylint: disable=protected-access
            return self._cards == other._cards
        return NotImplemented

    def remove(self, card: Card) -> None:
        """
        Remove a card from this container.

        :param card: card to remove
        """
        self._cards.remove(card)

    def add(self, card: Card) -> None:
        """
        Add a card to this container.

        :param card: card to add
        """
        if card in self._cards:
            raise KeyError(f'{card} already in set')
        self._cards.add(card)
