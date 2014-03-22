
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
    
    def init_turn(self, numRandom = 5):
        try:
            self.move_random_cards(self.deck, self.hand, numRandom)
        except:
            self.move_all_cards(self.discard, self.deck)
            self.move_random_cards(self.deck, self.hand, numRandom)
            
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

    def cleanup(self):
        self.move_all_cards(self.hand,   self.discard)
        self.move_all_cards(self.played, self.discard)
    
    def move_all_cards(self, fromPile, toPile):
        """Moves all cards from "fromPile" to "toPile"
        fromPile, toPile: collections.Coutner()
        """
        toPile.update(fromPile)
        fromPile.clear()
    
    def move_random_cards(self, fromPile, toPile, numRandom):
        """Moves numRandom cards from "fromPile" to "toPile"
        fromPile, toPile: collections.Coutner()
        """
        assert len(list(fromPile.elements())) >= numRandom
        elements = list(fromPile.elements())
        toMove = random.sample(elements, numRandom)
        toPile.update(toMove)
        fromPile.subtract(toMove)
    

        