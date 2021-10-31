"""Collections of cards"""
import random
from typing import final

from whist.core.cards.card import Card, Suit, Rank
from whist.core.cards.card_container import CardContainer


@final
class Deck(CardContainer):
    """An unordered collection of cards"""

    def pop_random(self) -> Card:
        """
        Removes one random card from deck.
        :return: A card from deck.
        :rtype: Card
        """
        card = random.choice(list(self._cards))
        self.remove(card)
        return card

    @staticmethod
    def empty():
        """
        Create an empty deck.

        :return: empty deck
        """
        return Deck()

    @staticmethod
    def full():
        """
        Create a full deck.

        :return: full deck
        """
        return Deck((Card(suit, rank) for suit in Suit for rank in Rank))
