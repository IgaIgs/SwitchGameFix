# CHANGELOG

* 1.1.5 [2019-11-19]: Bug fix release.
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