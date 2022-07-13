import random

import errors


class Deck:
    def __init__(self):
        self.__ranks = [
            'ace', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', 'jack', 'queen', 'king'
        ]
        self.__suits = {'hearts', 'spades', 'clubs', 'diamonds'}
        self.__cards = [(suit, rank) for rank in self.__ranks for suit in self.__suits]

    def __len__(self):
        return len(self.__cards)

    def __contains__(self, item):
        return item in self.__cards

    def __iter__(self):
        for card in self.__cards:
            yield card

    def __repr__(self):
        return str(self.__cards)

    def __bool__(self):
        return len(self) > 0

    def __add__(self, other):
        if isinstance(other, Deck):
            return self.__cards + other.__cards
        else:
            raise TypeError(f'Cannot combine a {type(self)} and a {type(other)}')

    def draw(self, amount=1):
        # Case: Attempting to draw more cards than in the deck
        if len(self) - amount < 0:
            raise errors.NoMoreCardsError('No more cards to draw!')

        # Draw the cards from the 'top'
        drawn_cards = self.__cards[:amount]

        # Remove the drawn cards
        self.__cards = [card for card in self if card not in drawn_cards]
        return drawn_cards

    def shuffle(self):
        self.__cards = random.sample(self.__cards, len(self))


if __name__ == '__main__':
    deck = Deck()
    deck1 = Deck()
    print(len(deck))
    deck += deck1
    print(len(deck))
