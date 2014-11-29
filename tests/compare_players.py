import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestComparePlayers(unittest.TestCase):

    def setUp(self):
        self.input = 'compare Sehwag and Dhoni'
        self.expected = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "and", "compare_word": "compare"}}'

        self.input_vs = 'Sehwag vs Dhoni'
        self.expected_vs = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "vs"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

        parser_2 = SentenceParser(self.input_vs)
        self.assertEqual(json.loads(self.expected_vs), json.loads(parser_2.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

