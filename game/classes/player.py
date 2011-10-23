

class Player (object):
    """The entity to store information about the player"""
    def __init__(self, player_id, name):
        super(Player, self).__init__()
        self.player_id = player_id
        self.name = name
        
        # A set of all the password IDs that we've built up
        self.passwords = set()
        
