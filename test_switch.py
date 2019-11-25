import switch

from cards import Card


class MockPlayer:
    """This is a class for AI players created just for the sake of running the tests.

    The players in this class always select the 1st possible choice in every situation.

    Attributes:
        name -- 'Mock player'
        hand -- hand of the mock player

    Methods: same as for real players but the choice is limited to whatever card or player is first.
    """
    is_ai = True

    def __init__(self, hand):
        """Constructor of the Mock Player class

        Parameters:
            name -- 'Mock player' is the name of all the mock players
        """
        self.name = "Mock player"
        self.hand = hand

    def select_card(self, choices, hands):
        """Select the first card in hand."""
        return choices[0]

    def ask_for_swap(self, others):
        """Swap hands with the first player."""
        return others[0]


def mock_setup_round(hands, stock, discards,
                     skip=False, draw2=False, draw4=False, direction=1):
    """Setup a mock round of the switch game.

    Starts a round of switch game by handing out cards to each of the mock players's hands,
    creating a stock pile and a discard pile. It also assigns all the game effects from switch.py
    module to new values which are used in this test file.

    Parameters:
        hands -- cards in each of the player's hand
        stock -- cards in the stock pile
        discards -- cards in the discard pile

    Keyword arguments:
        skip -- game effect when the next person in line is skipped
        draw2 -- game effect when the next person draws 2 cards
        draw4 -- game effect when the next person draws 4 cards
        direction -- the direction of the game

    Returns:
        A new mock round of the switch game.
    """
    def str_to_cards(spec):
        return [Card(sv[:1], sv[1:]) for sv in spec.split()]

    s = switch.Switch()
    s.players = [MockPlayer(str_to_cards(hand)) for hand in hands]
    s.discards = str_to_cards(discards)
    s.stock = str_to_cards(stock)
    s.skip = skip
    s.draw2 = draw2
    s.draw4 = draw4
    s.direction = direction
    return s


def test_setup_round__resets_flags():
    """Check whether the setup_round sets all flags to their initial values."""
    s = switch.Switch()
    s.players = [MockPlayer([]), MockPlayer([])]
    s.setup_round()
    assert s.skip is False
    assert s.draw2 is False
    assert s.draw4 is False
    assert s.direction == 1


def test_setup_round__deals_cards():
    """Check if setup_round deals correct number of cards."""
    s = switch.Switch()
    s.players = [MockPlayer([]), MockPlayer([])]
    s.setup_round()
    assert all(len(p.hand) == 7 for p in s.players)
    assert len(s.discards) == 1
    assert len(s.stock) == 52-len(s.players)*7-1


def test_pick_up_card__pick_correct_number():
    """Check if pick_up_card picks up correct number of cards."""
    s = mock_setup_round(['♣4', '♣9'], '♠7 ♢8 ♠5 ♢6 ♢7', '♠5 ♢6 ♡3')
    player = s.players[0]
    picked = s.pick_up_card(player, 4)
    assert picked == 4
    assert len(player.hand) == 5
    assert len(s.stock) == 1

    picked = s.pick_up_card(player, 4)
    assert picked == 3
    assert len(player.hand) == 8
    assert len(s.stock) == 0


def test_can_discard__follows_suit():
    """Check if can_discard properly judges which card is discardable by suit."""
    s = mock_setup_round([], '', '♣5')
    assert s.can_discard(Card('♣', '2'))
    assert s.can_discard(Card('♣', '3'))
    assert s.can_discard(Card('♣', '4'))
    assert s.can_discard(Card('♣', '6'))
    assert s.can_discard(Card('♣', '7'))
    assert s.can_discard(Card('♣', '8'))
    assert s.can_discard(Card('♣', '9'))
    assert s.can_discard(Card('♣', '10'))
    assert s.can_discard(Card('♣', 'J'))
    assert s.can_discard(Card('♣', 'K'))


def test_can_discard__follows_value():
    """Check if can_discard properly judges which card is discardable by value."""
    s = mock_setup_round([], '', '♣5')
    assert s.can_discard(Card('♢', '5'))
    assert s.can_discard(Card('♡', '5'))
    assert s.can_discard(Card('♠', '5'))


def test_can_discard__allows_ace():
    """Check if can_discard treats all Ace cards as always discardable."""
    s = mock_setup_round([], '', '♣5')
    assert s.can_discard(Card('♢', 'A'))
    assert s.can_discard(Card('♡', 'A'))
    assert s.can_discard(Card('♠', 'A'))


def test_can_discard__allows_queen():
    """Check if can_discard treats all Queen cards as always discardable."""
    s = mock_setup_round([], '', '♣5')
    assert s.can_discard(Card('♢', 'Q'))
    assert s.can_discard(Card('♡', 'Q'))
    assert s.can_discard(Card('♠', 'Q'))


def test_discard_card__sets_skip():
    """Check if discard_card sets switch.skip after card with value 8 has been discarded."""
    s = mock_setup_round(['♣4 ♡8', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.discard_card(s.players[0], Card('♡', '8'))
    assert s.skip


def test_discard_card__sets_draw2():
    """Check if can_discard makes the next player draw 2 cards after a card of value 2 has been discarded. """
    s = mock_setup_round(['♣4 ♡2', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.discard_card(s.players[0], Card('♡', '2'))
    assert s.draw2


def test_discard_card__sets_draw4():
    """Check if can_discard makes the next player draw 4 cards after a card of value 4 has been discarded. """
    s = mock_setup_round(['♣4 ♡Q', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.discard_card(s.players[0], Card('♡', 'Q'))
    assert s.draw4


def test_discard_card__reverses():
    """Check if discard_card reverses the game direction after a King card has been discarded."""
    s = mock_setup_round(['♣4 ♡K', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.discard_card(s.players[0], Card('♡', 'K'))
    assert s.direction == -1
    s.discard_card(s.players[1], Card('♣', 'K'))
    assert s.direction == 1


def test_discard_card__swaps():
    """Check if discard_card forces a hand swap between players after Jack card has been discarded."""
    s = mock_setup_round(['♣4 ♡J', '♣K ♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    s.discard_card(s.players[0], Card('♡', 'J'))
    assert s.players[0].hand == [Card('♣', 'K'), Card('♣', '9')]
    assert s.players[1].hand == [Card('♣', '4')]


def test_get_normalized_hand_sizes():
    """Check the correctness of hand size normalization."""
    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    assert s.get_normalized_hand_sizes(s.players[0]) == [1, 2, 3]
    assert s.get_normalized_hand_sizes(s.players[1]) == [2, 3, 1]
    assert s.get_normalized_hand_sizes(s.players[2]) == [3, 1, 2]

    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3', direction=-1)
    assert s.get_normalized_hand_sizes(s.players[0]) == [1, 3, 2]
    assert s.get_normalized_hand_sizes(s.players[1]) == [2, 1, 3]
    assert s.get_normalized_hand_sizes(s.players[2]) == [3, 2, 1]


def test_swap_hands():
    """Check if the hand swap is working right."""
    s = mock_setup_round(['♣4', '♣K ♣9', '♡J ♢5 ♢6'], '♢7 ♢8', '♡3')
    s.swap_hands(s.players[1], s.players[2])
    assert len(s.players[1].hand) == 3
    assert len(s.players[2].hand) == 2


def test_run_player__adheres_to_skip_flag():
    """Check if run_player adheres to switch.skip game effect."""
    from copy import deepcopy
    s = mock_setup_round(['', '', ''], '', '♣3', skip=True)
    player = s.players[1]
    hand_before = deepcopy(player.hand)
    s.run_player(player)
    assert player.hand == hand_before
    assert not s.skip


def test_run_player__adheres_to_draw2_flag():
    """Check if run_player adheres to switch.draw2"""
    s = mock_setup_round(['', ''], '♢5 ♣6 ♣7', '♢3', draw2=True)
    player = s.players[1]
    s.run_player(player)
    assert len(player.hand) == 2
    assert not s.draw2


def test_run_player__adheres_to_draw4_flag():
    """Check if run_player adheres to switch.draw4"""
    s = mock_setup_round(['', ''], '♢5 ♣5 ♣6 ♣7 ♣8', '♢3', draw4=True)
    player = s.players[1]
    s.run_player(player)
    assert len(player.hand) == 4
    assert not s.draw4


def test_run_player__returns_true_upon_win():
    """Check if run_player returns True if player wins"""
    s = mock_setup_round(['♣4 ♣5', '♣9', '♣10'], '♣6 ♣7 ♣8', '♣3')
    player = s.players[0]
    assert not s.run_player(player)
    assert s.run_player(player)


def test_run_player__draws_card():
    """Check if run_player forces pick up if no discard possible"""
    s = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♢8', '♡3')
    player = s.players[0]
    s.run_player(player)
    assert len(player.hand) == 2
    assert len(s.stock) == 3
    assert len(s.discards) == 1


def test_run_player__draws_card_and_discards():
    """Check if run_player discards drawn card if possible"""
    s = mock_setup_round(['♣4', '♣9'], '♢5 ♢6 ♢7 ♡8', '♡3')
    player = s.players[0]
    s.run_player(player)
    assert len(player.hand) == 1
    assert len(s.stock) == 3
    assert len(s.discards) == 2
