import random

class Deck:
    def __init__(self):
        self.__ranks = {
            'ace': [1, 14],
            '2': [2],
            '3': [3],
            '4': [4],
            '5': [5],
            '6': [6],
            '7': [7],
            '8': [8],
            '9': [9],
            '10': [10],
            'jack': [11],
            'queen': [12],
            'king': [13]
        }
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

    def draw(self, amount=1):
        # Case: Attempting to draw more cards than in the deck
        if len(self) - amount < 0:
            print('No more cards to draw!')
            return None

        # Draw the cards from the top
        drawn_cards = self.__cards[:amount]

        # Remove the drawn cards
        self.__cards = [card for card in self if card not in drawn_cards]
        return drawn_cards

    def shuffle(self):
        self.__cards = random.sample(self.__cards, len(self))

if __name__ == '__main__':
    deck = Deck()
    print(deck)
    print('='*100)
    print(deck.draw())
    # deck.shuffle()
    print(deck.draw())
    # deck.shuffle()
    print(deck.draw())
    # print(deck)
    # deck.shuffle()
    # print(deck)