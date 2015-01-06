import unittest
import os

from corpus.training.cricket_players import TrainCricketPlayers


class TestNameTraining(unittest.TestCase):

    def test_simple_names(self):
        training = TrainCricketPlayers(os.path.join(os.path.dirname(__file__), 'data', 'player_names.pickle'))
        tagged_words = training.get_names('what is the best score of dhoni and virat')
        self.assertListEqual(tagged_words, ['dhoni', 'virat'])

    def test_no_names(self):
        training = TrainCricketPlayers(os.path.join(os.path.dirname(__file__), 'data', 'player_names.pickle'))
        tagged_words = training.get_names('what is the best score of someone')
        self.assertListEqual(tagged_words, [])

if __name__ == '__main__':
    unittest.main()

