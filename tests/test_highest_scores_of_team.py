import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestHighestTeamScore(unittest.TestCase):

    def setUp(self):
        self.input = 'highest scores of england'
        self.expected = '{"scores": {"filler": {"filler1": {"filler": "scores"}, "filler2": {"filler": "of"}}, "team": {"team1": "england"}, "extent": "highest"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

