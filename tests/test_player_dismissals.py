import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache


class TestPlayerDismissals(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input = 'dismissals by bowled in india'
        self.expected = '{"player_dismissals": {"word_by": "by", "word_in": "in", "dismissals": "bowled", "word_dismissals": "dismissals", "team": {"team1": "india"}}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))


if __name__ == '__main__':
    unittest.main()

