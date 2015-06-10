import unittest

from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserAssert


class TestTeamChases(SentenceParserAssert):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input = 'when was the last time india chased 300+'
        self.expected = '{"matches_cond": {"word_chased": "chased", "last_time": {"word_was": "was", "word_the": "the", "word_when": "when", "word_last": "last", "word_time": "time"}, "target": "300+", "team": "india"}}'

        self.input_ground = 'how many times india chased 300+ in Chennai'
        self.expected_ground = '{"matches_cond": {"team": "india", "word_in": "in", "how_many_times": {"word_times": "times", "word_how": "how", "word_many": "many"}, "ground": {"ground1": "chennai"}, "word_chased": "chased", "target": "300+"}}'

    def test_search(self):
        self.assertParsedSentence(self.input, self.expected)

    def test_search_ground(self):
        self.assertParsedSentence(self.input_ground, self.expected_ground)


if __name__ == '__main__':
    unittest.main()

