import random
import user_interface as UI


class Player:
    """This is a class for all real players playing the game.

    This class creates the instances of the object Player when a real life player joins the game.
    It displays the information about the decisions of the player in regards to what card they choose
    and with whom do they want to swap.

    Attributes:
        name -- name of the player
        hand -- cards in the hand of the player

    Methods:
        select_card -- player's card selection
        ask_for_swap -- selection of who to swap hands with
    """
    is_ai = False

    def __init__(self, name):
        """Constructor for the Player class.

        Parameters:
            name -- the name of the player
        """
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        """Display what cards did the player choose from his hand."""
        return UI.select_card(choices)

    def ask_for_swap(self, others):
        """Display who the player asked for a swap of hands."""
        return UI.select_player(others)


class SimpleAI:
    """This is a class for bot players.

    This class creates instances of players who are not real life people but computer based AI players
    created within the game. Players in this class behave randomly.

    Attributes:
        name -- The name of the AI player.
        hand -- The set of cards in the AI player's 'hand'.

    Methods:
        select_card -- randomized card selection
        ask_for_swap -- randomized player selection for hand swap
    """
    is_ai = True

    def __init__(self, name):
        """Constructor for class SimpleAI.

        Parameters:
            name -- the name of the AI player.
        """
        self.name = name
        self.hand = []

    def select_card(self, choices, _):
        """Display what card was randomly chosen by the AI player."""
        return random.choice(choices)

    def ask_for_swap(self, others):
        """Display which player was randomly chosen to swap hands with the AI player."""
        return random.choice(others)


class SmartAI(SimpleAI):
    """This class contains bot players with predefined behaviour.

    This class creates instances of players who are not real life people but computer based AI players
    created within the game. Players in this class behave according to specified guidelines.

    Attributes:
        name -- The name of the AI player.
        hand -- The set of cards in the AI player's 'hand'.

    Methods:
        select_card -- intelligent card selection
        ask_for_swap -- intelligent selection of a player to swap hands with
    """
    def select_card(self, choices, hands):
        """Template for choosing a card to discard by the AI player.

        The card is chosen based on a scoring system, where the card with the highest score
        (and higher than -2) is chosen as the best candidate.

        Parameters:
            choices -- potential cards to be chosen
            hands -- cards in AI player's 'hand'
        """
        def score(card):
            """"Scoring system for the select_card function."""
            in_suit = len([c for c in self.hand
                           if c.suit == card.suit and c is not card])

            offset = {
                'J': 3*(hands[0]-1-min(hands[1:])),
                'Q': 6 + in_suit,
                '2': 4 + in_suit,
                '8': 2 + in_suit,
                'K': (3 if hands[-1] > hands[1] else -1) + in_suit,
                'A': -2 + in_suit,
            }

            return offset.get(card.value, in_suit)

        sorted_choices = sorted(choices, key=score, reverse=True)
        candidate = sorted_choices[0]
        return candidate if score(candidate) > -2 else None

    def ask_for_swap(self, others):
        """Template for how the AI player chooses the player to swap hands with.

        The player who has the least cards in their hand will be chosen for a swap.
        If there is more than one player with the same smallest hand size, the final choice
        will be done randomly.

        Parameters:
            others -- other players
        """
        smallest = min(len(p.hand) for p in others)
        best = [p for p in others if len(p.hand) == smallest]
        return random.choice(best)
