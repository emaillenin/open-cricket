import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserHelper


class TestPlayerDismissals(SentenceParserHelper):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input = 'dismissals by bowled in india'
        self.expected = '{"player_dismissals": {"word_by": "by", "word_in": "in", "dismissals": "bowled", "word_dismissals": "dismissals", "team": {"team1": "india"}}}'

    def test_search(self):
        self.assertParsedSentence(self.input, self.expected)


if __name__ == '__main__':
    unittest.main()

