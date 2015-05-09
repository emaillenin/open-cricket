import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache


class TestPlayerScores(unittest.TestCase):

    def setUp(self):
        SyntaxCache().build_cache()
        self.input_recent = 'what is the recent score of Suresh Raina'
        self.expected_recent = '{"scores": {"what_is_the": {"word_the": "the", "word_is": "is", "word_what": "what"}, "word_score": "score", "word_extent": "recent", "player": {"player2": "raina", "player1": "suresh"}, "word_of": "of"}}'

        self.input_highest = 'what is the highest score of Suresh Raina in t20 in 2015'
        self.expected_highest = '{"scores": {"what_is_the": {"word_the": "the", "word_is": "is", "word_what": "what"}, "word_score": "score", "word_extent": "highest", "player": {"player2": "raina", "player1": "suresh"}, "match_type": "t20", "word_in": "in", "word_of": "of", "year": "2015"}}'

    def test_search_recent(self):
        parser = SentenceParser(self.input_recent)
        self.assertEqual(json.loads(self.expected_recent), json.loads(parser.parse_sentence()))

    def test_search_highest(self):
        parser = SentenceParser(self.input_highest)
        self.assertEqual(json.loads(self.expected_highest), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

