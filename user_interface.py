#!/usr/bin/env python3


def say_welcome():
    """Print welcome information."""
    print_message("Welcome to Switch v1.1")


def print_game_menu():
    """Introduce the user to the menu options."""
    print("\nPlease select from one of the following options: [1-2]")
    print("1 - New Game")
    print("2 - Exit")


def print_player_info(player, top_card, hands):
    """Print player information.

    Parameters:
        player -- info about the player
        top_card -- top card on the discard pile
        hands -- cards in the hand of the player

    Returns:
        Information about the player's hand and what is the top discard card.
    """
    print("\nHANDS: " + str(hands))
    print("PLAYER: " + player.name)
    if not player.is_ai:
        print('HAND: ' + ', '.join(str(card) for card in player.hand))
    print('TOP CARD: ' + str(top_card))


def print_discard_result(discarded, card):
    """Print info about discard process.

    Parameters:
        discarded -- the card that has been discarded.
        card -- the card that was going to be discarded.

    Returns:
        Print statement about which card was discarded or that it wasn't possible to discard it.
        """
    if discarded:
        print("Discarded: " + str(card) + "\n")
    else:
        print("Unable to discard card: " + str(card))


def print_winner_of_game(player):
    """Print winner information.

    Parameters:
        player -- player who won

    Returns:
        Print a winning statement with the winner's name.
    """
    print_message('\n'+80*'-')
    print_message("Woohoo!!! Winner of the game is: " + player.name)
    print_message(80*'-')


def say_goodbye():
    """Say goodbye to the player."""
    print_message("Goodbye!")


def print_message(msg):
    print(msg)


# helper method for get_int_input method
def convert_to_int(string):
    """Converts string to int."""
    result = -1
    try:
        result = int(string)
    except Exception:
        pass
    return result


# methods get information from user
def get_int_input(min, max):
    """Get int value from user.

    Parameter:
        min -- the minimal integer value the player can input
        max -- the maximal integer value the player can input

    Returns:
        What integer did the player input.
    """
    choice = -1
    while choice < min or choice > max:
        print("> ", end="")
        choice = convert_to_int(input())
        if choice < min or choice > max:
            print(f"Try again: Input should be an integer between [{min:d}-{max:d}]")
    return choice


def get_string_input():
    """Get word from user."""
    print("> ", end="")
    s = input()
    return s


def get_player_information(MAX_PLAYERS):
    """Get player information.

    This method collects all the information about real life players who enter the game as well as
    creates AI players which need to enter the game for it to run (at least 2 players must be playing).
    It assigns names to the AI players and then chooses which will join current game.

    Parameters:
        MAX_PLAYERS -- the maximum number of players in this game (always 4).

    Returns:
        The final list of players playing the current game.
    """
    import random
    from players import Player, SimpleAI, SmartAI

    # create players list
    players = []
    # how many human players?
    print("\nHow many human players [1-4]:")
    no_of_players = get_int_input(1, MAX_PLAYERS)
    # for each player, get name
    for i in range(no_of_players):
        print("Please enter the name of player " + str(i + 1) + ":")
        players.append(Player(get_string_input()))

    ai_names = ['Angela', 'Bart', 'Charly', 'Dorothy']

    # how many AI players? ensure there are at least 2 players
    min = 1 if (len(players) == 1) else 0
    max = MAX_PLAYERS - no_of_players
    print(f"\nHow many ai players [{min:d}-{max:d}]:")
    no_of_players = get_int_input(min, max)
    # for each ai player, get name
    for name in ai_names[:no_of_players]:
        if random.choice([True, False]):
            players.append(SimpleAI(name))
        else:
            players.append(SmartAI("Smart "+name))

    return players


def select_card(cards):
    """Asks the player to select a card from their hand.

    Parameters:
        cards -- the cards in the player's hand.

    Returns:
        The card that has been chosen by the player.
    """
    print(f"Please select from one of the following cards: [1-{len(cards):d}]")
    for i, card in enumerate(cards, 1):
        print(str(i) + " - " + str(card))

    # get choice
    choice = get_int_input(0, len(cards))
    # get card
    if choice == 0:
        return None
    return cards[choice - 1]


def select_player(players):
    """Asks a player to select another player.

    Parameters:
        players -- a list of players currently playing the game.

    Returns:
        Which player has been chosen.
    """
    print(f"Please select from one of the following players: [1-{len(players):d}]")
    # print out for each player in players
    for i in range(len(players)):
        p = players[i]
        print(f"{i + 1:d} - {p.name}={len(p.hand):d}")

    # get choice
    choice = get_int_input(1, len(players))
    # get player
    return players[choice - 1]
