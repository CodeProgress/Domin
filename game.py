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
        self.player += 1
        self.player %= self.numPlayers
        
        
    def action_phase(self, player):
        pass
    
    def buy_phase(self, player):
        while player.numBuys > 0:
            # availCards = #fast look up, possibly heapq
            cardName = raw_input("Which card would you like to buy? ")
            cardName.lower()
            try:
                self.gameDeck.rem_one_card(cardName)
            except:
                print "{} is not in the deck".format(cardName)
            
            try:
                card = self.gameDeck.get_card(cardName)
                player.buy(card)
                print "{} successfully purchased".format(cardName)
            except AssertionError:
                print "Insufficient funds / no more buys"
            
    
    def cleanup_phase(self, player):
        player.cleanup()
    
    def turn(self, player):
        player.init_turn()
        self.action_phase(player)
        self.buy_phase(player)
        self.clean_up(player)

    def is_end_of_game(self):
        return self.gameDeck.get_card_count("province") == 0 \
                or self.gameDeck.numEmptyPiles >= 3
    

domin = Game(2)
domin.players[0].numCoins = 2
domin.buy_phase(domin.players[0])
