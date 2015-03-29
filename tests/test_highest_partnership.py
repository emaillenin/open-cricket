import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestPartnership(unittest.TestCase):

    def setUp(self):
        self.input = 'highest partnerships for 1st wicket for south africa'
        self.expected = '{"partnerships": {"wkt_order": "1st", "filler": "for", "wicket": "wicket", "word_extent": "highest", "team": {"team1": "south", "team2": "africa"}, "select": "partnerships"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

