

class PlayerNames():

    def __init__(self, player_names_file):
        with open(player_names_file) as f:
            self.player_names = frozenset(f.read().splitlines())

    def get_player_names(self, input_search):
        return [word.lower() for word in input_search.split(' ') if word in self.player_names]