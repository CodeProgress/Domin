import cards
import player

class Game(object):
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers

        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player())

        self.gameDeck = cards.Deck()
        
        self.playerToMoveNext = 0
        
        #to be continued
    
    def incr_player_to_move_next(self):
        self.player += 1
        self.player %= self.numPlayers
        
        
    def action_phase(self, player):
        pass
    
    def buy_phase(self, player):
        pass
    
    def cleanup_phase(self, player):
        pass
    
    def turn(self, player):
        self.action_phase(player)
        self.buy_phase(player)
        self.clean_up(player)

    def is_end_of_game(self):
        return self.gameDeck.deck['province'] == 0 \
                or self.gameDeck.numEmptyPiles >= 3
    
    

