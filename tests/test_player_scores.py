import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestPlayerScores(unittest.TestCase):

    def setUp(self):
        self.input_recent = 'Suresh Raina recent scores'
        self.expected_recent = '{"scores": {"period": "recent", "filler": "scores", "player": {"player1": "suresh","player2": "raina"}}}'

        self.input_highest = 'Suresh Raina highest scores'
        self.expected_highest = '{"scores": {"period": "highest", "filler": "scores", "player": {"player1": "suresh","player2": "raina"}}}'

    def test_search_recent(self):
        parser = SentenceParser(self.input_recent)
        self.assertEqual(json.loads(self.expected_recent), json.loads(parser.parse_sentence()))

    def test_search_highest(self):
        parser = SentenceParser(self.input_highest)
        self.assertEqual(json.loads(self.expected_highest), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

