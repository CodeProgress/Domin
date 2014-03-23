import cards
import player
import cProfile
import strategies

class Game(object):
    def __init__(self, numPlayers, AIPlayers = []):
        """numPlayers: int
        AIPlayers:  list of tuples: (name, strategy)
            name: string
            strategy: tuple: (buyStrategy, actionStrategy)
        """
        self.numPlayers = numPlayers

        startingDeck = ["estate"]*3 + ["copper"]*7

        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player("Player" + str(i), startingDeck))
        
        for i in AIPlayers:
            self.players.append(player.AIPlayer(i[0], i[1]))       
        
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
    
    def buy_phase(self, player, verbose = False):
        self.tally_coins(player)
        while player.numBuys > 0:
            
            if player.isAI:
                cardName = player.buyStrategy
            else:
                availCards = []
                for i in self.gameDeck.get_all_cards_below(player.numCoins):# key:price, value:card
                    if i in self.gameDeck.deck:
                        availCards.append(i)
                if verbose: print "It's your turn {}!".format(player.name)
                print "You have {} coins".format(player.numCoins)
                print "You can buy: {}".format(availCards)
                cardName = raw_input("Which card would you like to buy? ")
                cardName.lower()

            if cardName in self.gameDeck.deck: 
                try:
                    card = self.gameDeck.get_card(cardName)
                    player.buy(card)
                    self.gameDeck.rem_one_card(cardName)
                    if verbose: print "{} successfully purchased".format(cardName)
                except AssertionError:
                    print "Insufficient funds / no more buys"
                    break
            else:
                if verbose: print "{} is not in the deck".format(cardName)
                break
                
    def cleanup_phase(self, player):
        player.cleanup()
    
    def turn(self, player, verbose = False):
        player.init_turn()
        self.action_phase(player)
        self.buy_phase(player, verbose)
        self.cleanup_phase(player)

    def is_end_of_game(self):
        return "province" not in self.gameDeck.deck \
                or self.gameDeck.numEmptyPiles >= 3
                
    def play_game(self, verbose = False):
        """simulates game and returns list of tuples
        each tuple consists of (score, playerName)
        """
        while not self.is_end_of_game():
            player = self.players[self.playerToMoveNext]
            self.turn(player, verbose)
            self.incr_player_to_move_next()
        self.calc_scores()
        return sorted(self.find_winner(), reverse=True)
        
    def calc_scores(self):
        for player in self.players:
            player.numPoints = sum([self.gameDeck.get_card(card).pointVal for card in player.allCards.elements()])
    
    def find_winner(self):
        scores = sorted((player.numPoints, player.name) for player in self.players)
        return scores
        


def sim_games(numGames = 1000, numPlayers = 3):
    outcomes = []
    for i in range(numGames):
        domin = Game(numPlayers)
        outcomes.append(domin.play_game())
    
    print sorted(outcomes)[-1]

print sim_games()

#cProfile.run('sim_games()')

