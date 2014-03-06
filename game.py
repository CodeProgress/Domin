import cards
import player

class Game(object):
    def __init__(self, numPlayers):
        self.players = []
        for i in range(numPlayers):
            self.players.append(player.Player())
        
        #to be continued
        
    def action_phase(self):
        pass
    
    def buy_phase(self):
        pass
    
    def cleanup_phase(self):
        pass