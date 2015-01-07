import unittest
import os

from opencricket.chart.player_names import PlayerNames

class TestNameTraining(unittest.TestCase):

    def test_simple_names(self):
        user_search = 'dhoni and virat kohli stats'
        player_names = PlayerNames(os.path.join(os.path.dirname(__file__), 'data', 'player_names.txt')).get_player_names(user_search)
        self.assertListEqual(player_names, ['dhoni', 'virat', 'kohli'])

    def test_names_with_stats(self):
        user_search = 'dhoni wickets'
        player_names = PlayerNames(os.path.join(os.path.dirname(__file__), 'data', 'player_names.txt')).get_player_names(user_search)
        self.assertListEqual(player_names, ['dhoni'])

    def test_no_names(self):
        user_search = 'someone stats in world cup'
        player_names = PlayerNames(os.path.join(os.path.dirname(__file__), 'data', 'player_names.txt')).get_player_names(user_search)
        self.assertListEqual(player_names, [])

if __name__ == '__main__':
    unittest.main()

