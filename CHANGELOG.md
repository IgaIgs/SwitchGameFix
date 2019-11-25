# CHANGELOG

* v1.1.15 [2019-11-25]: Bug fix, documentation improvement and playable game release:
  - Created a game running module run_switch.py for clearer access to playing Switch.
  - Some minor changes in switch.py docstrings and a typo in test_switch.py
  - Fixed bugs in switch.py's run_round function :
   
   --> As the round progressed, the index of a player would go beyond the maximum list of players' indexes which is [0,1,2,3].
   
   --> Added a condition `if i == len(self.players) or i == (-(len(self.players))): i = 0`for when it reaches the limit,
   the index count will go back to the beginning (index = 0) to enable for multiple rounds of the game.
   
   --> Also, deleted an unnecessary condition for moving from one index to the next: % len(self.players) which was
   causing the game to crash.
   
  - Fixed bugs in run_player function in switch.py:
  
  --> The self.skip condition in run_player was only displaying a print statement without actually having any effect on the game.
  
  --> Fixed by putting a 'return None' statement in the condition.
  
  - Fixed bug for winner condition in run_player

  --> The winner of the game was chosen inadequately to the run of the round and to their hand because of 
  a lacking condition for winner in run_player.
  
  --> Added `if len(player.hand) == 0:` condition to make sure the winner is chosen only when they have discarded all 
  the cards from their hand.

* v1.1.14 [2019-11-22]: Improvements in the documentation release:
  - Completed docstrings for test_switch.py, user_interface.py and switch.py.
  - Corrected couple of typos in switch.py

* v.1.1.13 [2019-11-22]: Improvements in the documentation release:
  - Improved docstrings in cards.py
  - Improved and completed docstrings in players.py

* v1.1.12 [2019-11-21]: Improvements in the documentation release:
  - Completed docstrings for Card class in cards.py
  - Added docstrings for Player class in players.py

* v1.1.11 [2019-11-20]: Bug fix and documentation changes release:
  - Added some more details to v1.1.8 bug fix report.
  - Fixed a bug in switch.py's run_player function for self.draw2 and self.draw4 conditions
  
  --> `self.draw2 == False` and `self.draw4 == False` statements were checking the equivalency of the values on the 
  right and left sides of `==` instead of setting the right values to False.
  
  --> Changed `==` to `=` in both statements.

* v1.1.10 [2019-11-20]: Bug and typo fix release:
  - Fixed the typo in CHANGELOG.md update dates for the versions v.1.1.7-9 (month switched with day)
  - Fixed a bug in switch.py in run_player function in the discardable value
  
  --> The call to self.can_discard was working incorrectly resulting in cards being discarded even though they shouldn't
  
  --> Instead of using self.can_discard, specified what a discardable card is again based on what the current top card
  in the discard pile is: `discardable = [card for card in player.hand if card.value in 'QA' or 
  card.suit == top_card.suit or card.value == top_card.value]`

* v1.1.9 [2019-11-19]: Bug fix release:
  - Fixed a bug in switch.py in get_normalized_hand_sizes(self, player) function for reordering the list of players hand 
  sizes depending on chosen player.
  
  --> The list of normalized hand sizes was not properly displaying the chosen player's hand as the first in the list
  followed by all players after him (in game direction) because the code: `sizes = sizes[:idx] + sizes[idx:]` was basically
  only printing every hand size before and after the chosen player.
  
 --> Changed this line to: `sizes = sizes[idx:idx] + sizes[idx:] + sizes[:idx]`. Now the list includes the hand size of 
 the chosen player first and then all the next players' after him and before him (in that order, to make a whole circle)

* v1.1.8 [2019-11-19]: Bug fix release:
  - Fixed a bug in switch.py in run_player() function for executing the self.skip method.
  
  --> The `self.skip == False` statement had no effect: it was only checking the equivalency of self.skip and False, 
  not actually setting self.skip to False.
  
  --> Changed to `self.skip = False`.

* v1.1.7 [2019-11-19]: Bug fix release:
  - Fixed a bug in switch.py card_discard() for the game effect of card with value 'King'.
  
  --> Card 'King' should reverse the game direction but the condition in the above function was giving back the same 
  direction without any change due to a misuse of '*=' (self.direction was being multiplied by 1, which made no change).
  
  --> Changed the value of multiplication from 1 to -1 to allow for reversing the direction of the game:
   `elif card.value == 'K':
            self.direction *= -1`

* v1.1.6 [2019-11-19]: Bug (and typo) fix release:
  - Corrected the typo in CHANGELOG.md in the v.1.1.5 version (lacked 'v')
  - Fixed a bug in switch.py discard_card() function for the condition where card with value '2' is discarded
  
  --> The condition was supposed to make the next player draw 2 cards if the previous player discarded a '2' card. 
  However, the card value in this condition was '4' which obviously prevented the correct working of this function.
  
  --> Changed the card value from '4' to '2'.
 
* v1.1.5 [2019-11-19]: Bug fix release.
  - Fixed a bug in test_switch.py in test_can_discard__allows_ace()
  
  --> One of the asserts was a King card instead of Ace, therefore it was Failed
  
  --> Changed 'K' in card value to 'A': `assert s.can_discard(Card('♠', 'A'))`

* v1.1.4 [2019-11-19]: Bug fix release.
    - Fixed bug in switch.py's can_discard() function:
    
    --> The condition for whether a card can be discarded contained a mistake: instead of the card having to follow
    'suit' OR 'value' of the top card in the discard pile, the condition was set to AND, which prevented valid cards 
    from being discarded
    
    --> Changed 'and' to 'or' in the condition for discard: `else: top_card = self.discards[-1]
      return card.suit == top_card.suit or card.value == top_card.value`

* v1.1.3 [2019-11-19]: Bug fix release.
  - Fixed bug in switch.py's pick_up_card() function:
  
  --> The 'in range' method was causing another error and a more general bug fix solution than in the v1.1.1 was needed
  
  --> Fixed by adding '1' to the n parameter: `def pick_up_card(self, player, n=1):
        for i in range(1, n+1)`

* v1.1.2 [2019-11-19]: Bug fix release.
   - Fixed bug in cards.py in the Card class, which affected the generate_deck() function:
 
    --> There was a typo in the list of card values: A for 'Ace' was written twice, therefore the deck of cards had 56 cards
 (4suits * 14values) instead of 52 cards (4*13).
 
    --> Fixed by deleting the additional A from the value list: `values = '2 3 4 5 6 7 8 9 10 J Q K A'.split()`
    
* v1.1.1 [2019-11-19]: Bug fix release.
  - Fixed bug in switch.py in setup_round function:
  
  --> At the beginning of each round, 6 cards were dealt to each player's hand instead of 7 (as specified in the rules of the game)
  
  --> Fixed by: added 1 to the HAND_SIZE parameter in the def setup_round(self): self.pick_up_card function to make up for the 
  limitations of the 'in range': `for player in self.players: self.pick_up_card(player, HAND_SIZE+1)`
  
* v1.1.0 [2019-11-08]: Added a SmartAI computer opponent.
  Added strategy players.SmartAI
  None of the bugs have been fixed.

* v1.1.0 [2019-10-25]: First major release.
  This version is known to contain some bugs.
