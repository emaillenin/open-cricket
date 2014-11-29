import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestPlayerDismissals(unittest.TestCase):

    def setUp(self):
        self.input = 'dismissals by bowled by india'
        self.expected = '{"player_dismissals": {"filler": "by", "dismissals": "bowled", "what": "dismissals", "team": {"team1": "india"}}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

