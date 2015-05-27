import unittest

from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserAssert


class TestPlayerScores(SentenceParserAssert):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input_recent = 'what is the recent score of Suresh Raina'
        self.expected_recent = '{"scores": {"what_is_the": {"word_the": "the", "word_is": "is", "word_what": "what"}, "word_score": "score", "word_extent": "recent", "player": {"player2": "raina", "player1": "suresh"}, "word_of": "of"}}'

        self.input_highest = 'what is the highest score of Suresh Raina in t20 in 2015'
        self.expected_highest = '{"scores": {"what_is_the": {"word_the": "the", "word_is": "is", "word_what": "what"}, "word_score": "score", "word_extent": "highest", "player": {"player2": "raina", "player1": "suresh"}, "match_type": "t20", "word_in": "in", "word_of": "of", "year": "2015"}}'

    def test_search_recent(self):
        self.assertParsedSentence(self.input_recent, self.expected_recent)

    def test_search_highest(self):
        self.assertParsedSentence(self.input_highest, self.expected_highest)

if __name__ == '__main__':
    unittest.main()

