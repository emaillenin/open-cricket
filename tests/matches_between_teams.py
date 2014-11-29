import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestMatchesBetweenTeams(unittest.TestCase):

    def setUp(self):
        self.input = 'matches between india and england'
        self.expected = '{"matches": {"clause": {"CC": "and", "teamA": {"team": {"team1": "india"}}, "teamB": {"team": {"team1": "england"}}}, "select": "matches", "IN": "between"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

