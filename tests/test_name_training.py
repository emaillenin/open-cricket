import unittest
import os

from corpus.training.cricket_players import TrainCricketPlayers


class TestNameTraining(unittest.TestCase):

    def test_simple_names(self):
        training = TrainCricketPlayers(os.path.join(os.path.realpath('.'), 'data', 'player_names.pickle'))
        tagged_words = training.get_names('what is the best score of dhoni and virat')
        player_names = [p[0] for p in tagged_words if p[1] == 'NNP']
        self.assertListEqual(player_names, ['dhoni', 'virat'])

if __name__ == '__main__':
    unittest.main()

