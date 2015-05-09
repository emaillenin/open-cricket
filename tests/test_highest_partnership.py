import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache


class TestPartnership(unittest.TestCase):

    def setUp(self):
        SyntaxCache().build_cache()
        self.input = 'highest partnership for 1st wicket for south africa'
        self.expected = '{"partnerships": {"word_wkt_order": "1st", "word_wicket": "wicket", "word_for": "for", "word_extent": "highest", "team": {"team1": "south", "team2": "africa"}, "word_partnership": "partnership"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

