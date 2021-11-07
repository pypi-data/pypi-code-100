# Import the typing library so variables can be type cast
from typing import List, Tuple

import itertools
import random

# Define the cards & deck variable type structure
_Card_ = Tuple[str, str]
_Deck_ = List[_Card_]
# Define a hand as a collection of cards, like a deck
_Hand_ = List[_Card_]

# Define the number of cards in the deck
STANDARD_DECK_SIZE: int = 52

# Define the card suite types
STANDARD_SUITES: List[str] = ["Hearts", "Clubs", "Diamonds", "Spades"]
# Define the card deck picture/face cards
STANDARD_FACE_CARDS: List[str] = [
    "J",  # Jack
    "Q",  # Queen
    "K",  # King
    "A",  # Ace
]


def shuffle_deck(deck: _Deck_) -> _Deck_:
    """Generate a new shuffled verson of the card deck"""
    # Copy the original so we don't mutate it
    _deck: _Deck_ = deck.copy()
    # Shuffle & return the copy of the deck
    random.shuffle(_deck)
    return _deck


def draw_card(deck: _Deck_, cards: int = 1) -> Tuple[_Hand_, _Deck_]:
    # draw the top x number of cards from the start of the deck list
    drawn: _Hand_ = deck[:cards]
    # This reshuffles the deck so is not good for this purpose
    # because it creates a new unordered list
    # We need to just, pop/slice/unshift the cards from the top/staart
    # of the deck list
    deck_remaining: _Deck_ = list(set(set(deck) - set(drawn)))
    return drawn, deck_remaining


def new_deck() -> _Deck_:
    """Create a new deck of cards"""
    # Generate the list of numbers from 2 to 10 & add the picture cards
    ranks: List[_Card_] = [
        str(rank) for rank in list(range(2, 11)) + STANDARD_FACE_CARDS
    ]
    # Create a list of ranked cards combined with suite
    deck: _Deck_ = [card for card in itertools.product(STANDARD_SUITES, ranks)]
    return deck


def new_shuffled_deck() -> _Deck_:
    """Generate a new shuffled deck of cards"""
    return shuffle_deck(new_deck())


def main() -> None:
    """Main function to run the application"""
    deck = new_shuffled_deck()
    for idx, card in enumerate(deck):
        print(f"Card {idx+1} is {card[1]} of {card[0]}")
    drawn, deck_remaining = draw_card(deck, cards=5)
    print(drawn)
    for idx, card in enumerate(deck_remaining):
        print(f"Card {idx+1} is {card[1]} of {card[0]}")


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
