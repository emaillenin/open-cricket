import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserAssert


class TestHighestTeamScore(SentenceParserAssert):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input = "what is the highest score of england"
        self.expected = '{"scores": {"team": "england", "what_is_the": {"word_is": "is", "word_what": "what", "word_the": "the"}, "word_score": "score", "word_extent": "highest", "word_of": "of"}}'

        self.input_in_this_year = "what is the highest score of england in this year"
        self.expected_in_this_year = '{"scores": {"word_year": "year", "word_this_last": "this", "word_in": "in", "team": "england", "what_is_the": {"word_is": "is", "word_what": "what", "word_the": "the"}, "word_score": "score", "word_extent": "highest", "word_of": "of"}}'

        self.input_highest_single_team = "what is the highest score of a team"
        self.expected_highest_single_team = '{"scores": {"word_a": "a", "word_team": "team", "what_is_the": {"word_is": "is", "word_what": "what", "word_the": "the"}, "word_score": "score", "word_extent": "highest", "word_of": "of"}}'

    def test_search(self):
        self.assertParsedSentence(self.input, self.expected)

    def test_search_in_this_year(self):
        self.assertParsedSentence(self.input_in_this_year, self.expected_in_this_year)

    def test_search_highest_single_team (self):
        self.assertParsedSentence(self.input_highest_single_team, self.expected_highest_single_team)

if __name__ == "__main__":
    unittest.main()

