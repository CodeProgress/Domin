
import collections
import random

class Player(object):
    def __init__(self, name, startingDeck):
        """
        name: String
        startingDeck: list of card names (Strings)
        """
        self.name  = name
        
        #players hand will only contain references to the card object (its name)
        #collections.Counter() will be faster for calcing probabilities
        self.deck    = collections.Counter(startingDeck)
        self.hand    = collections.Counter()
        self.played  = collections.Counter()
        self.discard = collections.Counter()
        
        
        #turn
        self.numActions = 1
        self.numBuys    = 1
        self.numCoins   = 0
        self.numPoints  = 0
        
        #overall
        self.allCards    = collections.Counter(startingDeck)
        self.totalPoints = 0
    
    # deck_to_hand
    # hand_to_played
    # hand_to_discard
    # played_to_discard
    # discard_to_deck
    # 
    
    def init_turn(self, numToDraw = 5):
        try:
            self.move_random_cards(self.deck, self.hand, numToDraw)
        except:
            self.move_all_cards(self.discard, self.deck, numToDraw)
            self.move_random_cards(self.deck, self.hand, numToDraw)
            
        self.numActions = 1
        self.numBuys    = 1
        self.numCoins   = 0
        self.numPoints  = 0
    
    def act(self, action):
        action()
        self.numActions -= 1
    
    def buy(self, card):
        assert self.numBuys > 0 and self.numCoins >= card.cost
        self.discard[card.name] += 1
        self.allCards[card.name] += 1
        self.numCoins -= card.cost
        self.numBuys -= 1
    
    def move_all_cards(fromPile, toPile):
        """Moves all cards from "fromPile" to "toPile"
        fromPile, toPile: collections.Coutner()
        """
        toPile.update(fromPile)
        fromPile.clear()
    
    def move_random_cards(fromPile, toPile, numRandom):
        """Moves all cards from "fromPile" to "toPile"
        fromPile, toPile: collections.Coutner()
        """
        assert len(list(fromPile.elements())) >= numRandom
        for i in range(numRandom):
            toMove = random.choice(fromPile.elements())
            toPile.update(toMove)
            fromPile.subtract(toMove)
    
    def cleanup(self):
        self.move_all_cards(self.hand,   self.discard)
        self.move_all_cards(self.played, self.discard)
        