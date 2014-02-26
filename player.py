
import collections

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
        