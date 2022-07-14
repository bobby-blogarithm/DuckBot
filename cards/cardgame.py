import random
from abc import ABC, abstractmethod

import errors
from .deck import Deck


class CardGame(ABC):
    def __init__(self, max_players):
        self.deck = Deck()
        self.max_players = max_players
        self.players = {}

    @abstractmethod
    def turn(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    def join(self, player):
        if len(self.players) + 1 > self.max_players:
            self.players.add(player)
        else:
            raise errors.MaxPlayerLimitError('No more seats left')

    def leave(self, player):
        if player in self.players:
            self.players.remove(player)
        else:
            raise ValueError('Player not in game')


class CardGamePlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add(self, cards):
        self.hand += cards

    def remove(self, cards):
        for card in cards:
            self.hand.remove(card)

    def remove_random(self, amount=1):
        # Case: Attempting to draw more cards than in the deck
        if len(self) - amount < 0:
            raise errors.NoMoreCardsError('No more cards to draw!')

        # Remove an amount of random cards
        drawn_cards = random.sample(self.hand, amount)

        # Remove the drawn cards
        self.hand = [card for card in self if card not in drawn_cards]
        return drawn_cards

    def shuffle(self):
        self.hand = random.sample(self.hand, len(self.hand))
