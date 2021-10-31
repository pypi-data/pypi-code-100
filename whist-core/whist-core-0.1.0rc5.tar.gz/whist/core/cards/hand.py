"""Hand held by player."""
from typing import final

from whist.core.cards.card import Suit
from whist.core.cards.card_container import CardContainer


@final
class Hand(CardContainer):
    """
    Hand of player during a game.
    """
    @staticmethod
    def empty():
        """
        Creates a empty hand.
        :return: empty hand
        :rtype: Hand
        """
        return Hand()

    def contains_suit(self, suit: Suit) -> bool:
        """
        Checks if a card of a suit is still in the hand.
        :param suit: which should be checked
        :type suit: Suit
        :return: True if contains this suit else False
        :rtype: bool
        """
        if len(self._cards) == 0:
            return False
        return any((card for card in self._cards if card.suit == suit))
