
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
        self.action   = action

                                
#methods to create cards

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


