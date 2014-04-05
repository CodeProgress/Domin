#need to find a way to pass the game information ro the action cards.
#possivly using the game object, but should find another way...

class Card(object):
    def __init__(self, name, cost, cardType, 
                 coinVal = 0, pointVal = 0, action = None
                 ):
        """
        name     : String
        cost     : int
        cardType : "t" or "v" (for treasure or victory)
        coinVal  : int
        pointVal : int
        action   : function
        """
        self.name     = name
        self.cost     = cost
        self.cardType = cardType
        self.coinVal  = coinVal
        self.pointVal = pointVal
        self.action   = action     #function
        

class Deck(object):
    def __init__(self, numPlayers = 2):
        self.deck = {}
        self.numEmptyPiles = 0
        
        #Treasure cards
        self.gold   = gold()
        self.silver = silver()
        self.copper = copper()
        
        #Victory cards
        self.province = province()
        self.duchy    = duchy()
        self.estate   = estate()

        if numPlayers > 3:
            numTreasure = 12
        else:
            numTreasure = 8

        self.deck[self.gold.name]   = [30, self.gold]
        self.deck[self.silver.name] = [40, self.silver]
        self.deck[self.copper.name] = [60, self.copper]

        self.deck[self.province.name] = [numTreasure, self.province]
        self.deck[self.duchy.name]    = [numTreasure, self.duchy]
        self.deck[self.estate.name]   = [numTreasure, self.estate]
        
        self.origDeck = self.deck.copy()
        
        self.cardsByCost = self.create_cards_by_cost()

        self.mostExpensiveCard = max(self.cardsByCost.keys())
        
        self.allCardsBelow = self.create_all_cards_below()
    
    def rem_one_card(self, cardName):
        """subtracts 1 card from cardName pile in deck
        if remaining pile is empty, cardName is deleted from deck and
        self.numEmptyPiles is incremented by 1
        """
        if cardName in self.deck:
            self.deck[cardName][0] -= 1
            if self.get_card_count(cardName) == 0:
                self.deck.pop(cardName)
                self.numEmptyPiles += 1
        else:
            raise NameError("Card {} does not exist".format(cardName))
    
    def get_card_count(self, cardName):
        """Returns the number of cards in the deck named cardName
        cardName: String
        If cardName not in deck, raises NameError
        """
        if cardName in self.deck:
            return self.deck[cardName][0]
        else:
            raise NameError("Card {} does not exist".format(cardName))
    
    def get_card(self, cardName):
        """Returns the card object
        cardName:  String
        If cardName not in origDeck, raises NameError
        """
        if cardName in self.origDeck:
            return self.origDeck[cardName][1]
        else:
            raise NameError("Card {} does not exist".format(cardName))

    def create_cards_by_cost(self):
        cardsByCost = {}
        for i in self.deck.values():
            card = i[1]
            if card.cost in cardsByCost:
                cardsByCost[card.cost].append(card.name)
            else:
                cardsByCost[card.cost] = [card.name]
        return cardsByCost
    
    def get_cards_by_cost(self, cost):
        if cost in self.cardsByCost:
            return self.cardsByCost[cost]
        return []
        
    def create_all_cards_below(self):
        """Precompute lists of all cards that can be bought"""
        allCosts = range(self.mostExpensiveCard + 1)
        allCardsBelow = {i:[] for i in allCosts}
        
        for i in allCosts:
            for j in allCosts[:i+1]:
                allCardsBelow[i].append(self.get_cards_by_cost(j))
            #flatten list of lists
            allCardsBelow[allCosts[i]] = reduce(lambda x,y: x+y, allCardsBelow[allCosts[i]])
        return allCardsBelow
    
    def get_all_cards_below(self, numCoins):
        if numCoins in self.allCardsBelow:
            return self.allCardsBelow[numCoins]
        if numCoins <= 0:
            return []
        else:
            return self.allCardsBelow[self.mostExpensiveCard]
        
        
#methods to create cards (avoid globals)

#Treasure cards
def gold():
    return Card("gold",     6, "t", 3, 0)

def silver():
    return Card("silver",   3, "t", 2, 0)

def copper():
    return Card("copper",   1, "t", 1, 0)

#Victory cards
def province():
    return Card("province", 8, "v", 0, 6)

def duchy():
    return Card("duchy",    5, "v", 0, 3)

def estate():
    return Card("estate",   2, "v", 0, 1)


##Special Victory cards
#def Gardens():
#    """Worth 1 Victory for every 10 cards in your deck (rounded down)"""
#    pass
##Action cards (ordered by price)
#def Cellar():
#    """+1 Action
#    Discard any number of cards.
#    +1 Card per card discarded
#    """
#    pass
#    
#def Chapel():
#    """Trash up to 4 cards from your hand"""
#    pass
#    
#def Moat():
#    """+2 Cards
#    When another player plays an Attack card, 
#    you may reveal this from your hand. 
#    If you do, you are unaffected by that Attack
#    """
#    pass
#    
#def Chancellor():
#    """+$2, You may immediately put your deck into your discard pile"""
#    pass
#
def Village(game):
    """+1 Card; +2 Actions"""
    player = game.get_current_player()
    player.move_random_cards(player.deck, player.hand, 1)
    player.numActions += 1

def Woodcutter(game):
    """+1 Buy; +$2"""
    player = game.get_current_player()
    player.numBuys += 1
    player.numCoins += 2
#
#def Workshop():
#    """Gain a card costing up to $4"""
#    pass
#
#def Bureaucrat():
#    """Gain a silver card; put it on top of your deck. 
#    Each other player reveals a Victory card from his hand and 
#    puts it on his deck (or reveals a hand with no Victory cards)"""
#    pass
#    
#def Feast():
#    """Trash this card. Gain a card costing up to $5"""
#    pass
#
#def Militia():
#    """+$2
#    Each other player discards down to 3 cards in his hand"""
#    pass
#
#def Moneylender():
#    """Trash a Copper from your hand. If you do, +$3"""
#    pass
#
#def Remodel():
#    """Trash a card from your hand. 
#    Gain a card costing up to $2 more than the trashed card"""
#    pass
#    
def Smithy(game):
    """+3 Cards"""
    player = game.get_current_player()
    player.move_random_cards(player.deck, player.hand, 3)
#
#def Spy():
#    """+1 Card; +1 Action
#    Each player (including you) reveals the top card of his deck and 
#    either discards it or puts it back, your choice"""
#    pass
#    
#def Thief():
#    """Each other player reveals the top 2 cards of his deck. 
#    If they revealed any Treasure cards, they trash one of them that you choose. 
#    You may gain any or all of these trashed cards. 
#    They discard the other revealed cards"""
#    pass
#
#def ThroneRoom():
#    """Choose an Action card in your hand. Play it twice"""
#    pass
#
#def CouncilRoom():
#    """+4 Cards; +1 Buy
#    Each other player draws a card"""
#    pass
#
def Festival(game):
    """+2 Actions, +1 Buy; +$2"""
    player = game.get_current_player()
    player.numActions += 2
    player.numBuys += 1
    player.numCoins += 2
    

def Laboratory(game):
    """+2 Cards; +1 Action"""
    player = game.get_current_player()
    player.move_random_cards(player.deck, player.hand, 2)
    player.numActions += 1


#    
#def Library():
#    """Draw until you have 7 cards in hand. 
#    You may set aside any Action cards drawn this way, as you draw them; 
#    discard the set aside cards after you finish drawing"""
#    pass
    
def Market(game):
    """+1 Card; +1 Action; +1 Buy; +$1"""
    player = game.get_current_player()
    player.move_random_cards(player.deck, player.hand, 1)
    player.numActions += 1
    player.numBuys += 1
    player.numCoins += 1

#def Mine():
#    """Trash a Treasure card from your hand. 
#    Gain a Treasure card costing up to $3 more; 
#    put it into your hand"""
#    pass
#
#def Witch():
#    """+2 Cards
#    Each other player gains a Curse card"""
#    pass
#    
#def Adventurer():
#    """Reveal cards from your deck until you reveal 2 Treasure cards. 
#    Put those Treasure cards in your hand and discard the other revealed cards
#    """
#    pass
#
#
