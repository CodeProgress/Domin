import cards
import player

class Game(object):
    def __init__(self, numPlayers):
        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player())
        
        #to be continued
        
        self.gameDeck = cards.Deck()
   
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
        assert self.gameDeck.deck['province'] >= 0

        return self.gameDeck.deck['province'] == 0
    
    

