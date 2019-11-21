from collections import namedtuple


class Card(namedtuple('CardData', ['suit', 'value'])):
    """This is a class for all cards in a deck displayed in tuples.

    Constructor:
    def __new__(cls, suit, value):
        :param cls: Card class reference.
        :param suit: The suit of the card instance.
        :param value: The value of the card instance.
        :return: An instance of card object with specified suit and value.

    Attributes:
    suit -- The suit of the card.
    value -- The value of the card.

    Methods:
    __str__ -- Description of class attributes.
    """
    suits = '♣ ♢ ♡ ♠'.split()
    values = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    def __new__(cls, suit, value):
        assert suit in cls.suits
        assert value in cls.values
        return super().__new__(cls, suit, value)

    def __str__(self):
        """String representation method for Card class."""
        return '{} {}'.format(self.suit, self.value)


def generate_deck():
    """Generate sorted full deck of cards"""
    return [Card(suit, value)
            for suit in Card.suits for value in Card.values]
