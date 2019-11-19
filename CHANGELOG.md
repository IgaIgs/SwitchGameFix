# CHANGELOG

* v1.1.0 [2019-11-08]: Added a SmartAI computer opponent.
  Added strategy players.SmartAI
  None of the bugs have been fixed.

* v1.1.0 [2019-10-25]: First major release.
  This version is known to contain some bugs.

* v1.1.1 [2019-11-19]: Bug fix release.
  - Fixed bug in switch.py in setup_round function:
  
  --> At the beginning of each round, 6 cards were dealt to each player's hand instead of 7 (as specified in the rules of the game)
  
  --> Fixed by: added 1 to the HAND_SIZE parameter in the def setup_round(self): self.pick_up_card function to make up for the 
  limitations of the 'in range': `for player in self.players: self.pick_up_card(player, HAND_SIZE+1)`
 
 * v1.1.2 [2019-11-19]: Bug fix release.
   - Fixed bug in cards.py in the Card class, which affected the generate_deck() function:
 
    --> There was a typo in the list of card values: A for 'Ace' was written twice, therefore the deck of cards had 56 cards
 (4suits * 14values) instead of 52 cards (4*13).
 
    --> Fixed by deleting the additional A from the value list: `values = '2 3 4 5 6 7 8 9 10 J Q K A'.split()`
  