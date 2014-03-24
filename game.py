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

        startingDeck = ["estate"]*3 + ["copper"]*7

        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player("Player" + str(i), startingDeck))
        
        for i in AIPlayers:
            name = i[0]
            strategy = i[1]
            self.players.append(player.AIPlayer(name, startingDeck, strategy))       
        
        self.numPlayers = len(self.players)
        
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
        #consider making this more modular
        self.tally_coins(player)
        while player.numBuys > 0:
            
            if player.isAI:
                cardName = player.buyStrategy(player.numCoins)
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
    
    def reset_all(self, numPlayers, AIPlayers = []):
        self.__init__(numPlayers, AIPlayers)
    

def sim_games(numGames = 1000, AIPlayers = []):
    outcomes = []
    domin = Game(0, AIPlayers)
    for i in range(numGames):
        outcomes.append(domin.play_game())
        domin.reset_all(0, AIPlayers)
    
    sorted_outcomes = sorted(outcomes)
    extremes = sorted_outcomes[-1], sorted_outcomes[0]
    print extremes

AIPlayers = [("Buy Provinces", (strategies.buy_only_prov, None)),
             ("Buy Best Avail", (strategies.buy_best_avail, None))]

#print sim_games(AIPlayers = AIPlayers)

cProfile.run('sim_games(AIPlayers = AIPlayers)', sort = 'cumtime')

