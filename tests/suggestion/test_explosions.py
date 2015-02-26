import unittest
import json

from opencricket.suggestion.productions import Productions

class TestExplosions(unittest.TestCase):

    def setUp(self):
        self.input = 'compare sehwag and dhoni'
        self.expected = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "and", "compare_word": "compare"}}'

        self.input_compare_year = 'compare Sehwag vs Dhoni in 2011'
        self.expected_compare_year = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs", "compare_word": "compare", "word_in": "in","year": "2011"}}'

        self.input_compare_in_match_type = 'compare Sehwag vs Dhoni in test'
        self.expected_compare_match_type = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs", "compare_word": "compare","word_in": "in", "match_type": "test"}}'

    def test_explosions(self):
        parser = Productions().explode('/Users/leninraj/projects/oc_data/expansions', '/Users/leninraj/projects/oc_data/exploded')


if __name__ == '__main__':
    unittest.main()

