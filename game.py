import cards
import player
import cProfile
import strategies
import pylab

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
    

def sim_games(numGames = 100, AIPlayers = []):
    outcomes = []
    domin = Game(0, AIPlayers)
    for i in range(numGames):
        outcomes.append(domin.play_game())
        domin.reset_all(0, AIPlayers)
    
    return outcomes

def count_wins(outcomes):
    """returns a list of reverse sorted tuples (score, strategy)"""
    counter = {x[1]:0 for x in outcomes[0]}
    numPlayers = len(outcomes[0])
    
    for game in outcomes:
        
        index = 0
        toScore = numPlayers
        counter[game[index][1]] += toScore
        index += 1
        while index < numPlayers:
            if game[index][0] == game[index - 1][0]:
                counter[game[index][1]] += toScore
            else:
                toScore -= 1
                counter[game[index][1]] += toScore
            index += 1

    return [(x, counter[x]) for x in sorted(counter,
                                             reverse = True, 
                                             key = lambda y: counter[y])]
           

def plot_outcomes(outcomes):
    """plots the output from count_wins as a barchart"""
    outcomes = zip(*outcomes)
    players = outcomes[0]
    results = outcomes[1]
    numPlayers = len(players)
    
    x = range(numPlayers)
    y = results
    f = pylab.figure()

    ax = f.add_axes([0.1, 0.2, 0.8, 0.7])
    ax.bar(x, y, align='center')
    ax.set_xticks(x)
    ax.set_xticklabels(players, rotation = 15)
    
    pylab.title("How did everyone do?")
    pylab.ylabel("Number of Wins")
    f.show()



if __name__ == "__main__":
    buyProvNotCopper      = ("Buy Prov (but not copper)", 
                                (strategies.buy_only_prov_no_copper, None))      
    buyProv               = ("Buy Prov", (strategies.buy_only_prov, None))  
    buyBestAvailNotCopper = ("Buy Best Avail (but not copper)", 
                                (strategies.buy_best_avail_no_copper, None))
    buyBestAvail          = ("Buy Best Avail", (strategies.buy_best_avail, None))
    
            
    AIPlayers = [buyProvNotCopper, buyProv, buyBestAvailNotCopper, buyBestAvail]
    
    allGames = sim_games(AIPlayers = AIPlayers)
    
    plot_outcomes(count_wins(allGames))
    
    #cProfile.run('sim_games(AIPlayers = AIPlayers)', sort = 'cumtime')



