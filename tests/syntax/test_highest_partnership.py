import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserAssert


class TestPartnership(SentenceParserAssert):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input = 'highest partnership for 1st wicket for south africa'
        self.expected = '{"partnerships": {"word_wkt_order": "1st", "word_wicket": "wicket", "word_for": "for", "word_extent": "highest", "team": "south africa", "word_partnership": "partnership"}}'

    def test_search(self):
        self.assertParsedSentence(self.input, self.expected)

if __name__ == '__main__':
    unittest.main()

