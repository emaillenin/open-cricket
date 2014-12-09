import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestComparePlayers(unittest.TestCase):

    def setUp(self):
        self.input = 'compare Sehwag and Dhoni'
        self.expected = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "and", "compare_word": "compare"}}'

        self.input_vs = 'Sehwag vs Dhoni'
        self.expected_vs = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs"}}'

        self.input_compare_year = 'compare Sehwag vs Dhoni in 2011'
        self.expected_compare_year = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs", "compare_word": "compare", "filler": "in", "year": "2011"}}'

        self.input_compare_in_match_type = 'compare Sehwag vs Dhoni in test'
        self.expected_compare_match_type = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs", "compare_word": "compare", "filler": "in", "match_type": "test"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_vs(self):
        parser_2 = SentenceParser(self.input_vs)
        self.assertEqual(json.loads(self.expected_vs), json.loads(parser_2.parse_sentence()))

    def test_compare_in_a_year(self):
        parser = SentenceParser(self.input_compare_year)
        self.assertEqual(json.loads(self.expected_compare_year), json.loads(parser.parse_sentence()))

    def test_compare_in_a_match_type(self):
        parser = SentenceParser(self.input_compare_in_match_type)
        self.assertEqual(json.loads(self.expected_compare_match_type), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

