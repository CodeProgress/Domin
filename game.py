import cards
import player

class Game(object):
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers

        startingDeck = ["estate"]*3 + ["copper"]*7

        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player("Player" + str(i), startingDeck))

        self.gameDeck = cards.Deck()
        
        self.playerToMoveNext = 0
        
        #to be continued
    
    def incr_player_to_move_next(self):
        self.playerToMoveNext += 1
        self.playerToMoveNext %= self.numPlayers
    
    
    def tally_coins(self, player):
        total = 0
        for card in player.played.elements():
            total += self.gameDeck.get_card(card).coinVal
        for card in player.hand.elements():
            total += self.gameDeck.get_card(card).coinVal
        player.numCoins = total
        
    def action_phase(self, player):
        pass
    
    def buy_phase(self, player):
        self.tally_coins(player)
        while player.numBuys > 0:
            #availCards = []
            #for i in self.gameDeck.get_all_cards_below(player.numCoins):# key:price, value:card
            #    if i in self.gameDeck.deck:
            #        availCards.append(i)
            print "It's your turn {}!".format(player.name)
            #print "You have {} coins".format(player.numCoins)
            #print "You can buy: {}".format(availCards)
            #cardName = raw_input("Which card would you like to buy? ")
            #cardName.lower()
            
            cardName = self.strat_only_buy_prov(player)

            if cardName in self.gameDeck.deck: 
                try:
                    card = self.gameDeck.get_card(cardName)
                    player.buy(card)
                    self.gameDeck.rem_one_card(cardName)
                    print "{} successfully purchased".format(cardName)
                except AssertionError:
                    print "Insufficient funds / no more buys"
            else:
                print "{} is not in the deck".format(cardName)
    
    def cleanup_phase(self, player):
        player.cleanup()
    
    def turn(self, player):
        player.init_turn()
        self.action_phase(player)
        self.buy_phase(player)
        self.cleanup_phase(player)

    def is_end_of_game(self):
        return "province" not in self.gameDeck.deck \
                or self.gameDeck.numEmptyPiles >= 3
                
    def play_game(self):
        while not self.is_end_of_game():
            player = self.players[self.playerToMoveNext]
            self.turn(player)
            self.incr_player_to_move_next()
        self.calc_scores()
        print self.find_winner()
        
    def calc_scores(self):
        for player in self.players:
            player.numPoints = sum([self.gameDeck.get_card(card).pointVal for card in player.allCards.elements()])
    
    def find_winner(self):
        scores = sorted((player.numPoints, player.name) for player in self.players)
        return scores[-1]
    
    def strat_only_buy_prov(self, player):
        """strategy where player only buys provinces if numCoins >= 8
        otherwise, player buys the most valuable treasure card.
        returns the card to buy (as String) if numCoins > 0, else returns None
        """
        coins = player.numCoins
        if coins >= 8:
            return "province"
        if coins >= 6:
            return "gold"
        if coins >= 3:
            return "silver"
        if coins >= 1:
            return "copper"
        return None
    
        

domin = Game(2)
#domin.players[0].numCoins = 11
#domin.players[0].numBuys = 2
#domin.turn(domin.players[0])

domin.play_game()

