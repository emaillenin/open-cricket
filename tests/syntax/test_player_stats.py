import unittest

from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserHelper


class TestPlayerStats(SentenceParserHelper):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input_stats = 'Dale Steyn stats'
        self.expected_stats = '{"player_stats": {"player": {"player2": "steyn", "player1": "dale"}, "word_stats": "stats"}}'

        self.input_stats_as_captain = 'Dale Steyn stats as captain'
        self.expected_stats_as_captain = '{"player_stats": {"player": {"player2": "steyn", "player1": "dale"}, "word_stats": "stats", "word_as": "as", "word_captain": "captain"}}'

        self.input_series = 'Dale Steyn stats in ipl'
        self.expected_series = '{"player_stats": {"word_stats": "stats", "series": {"series1": "ipl"}, "player": {"player1": "dale", "player2": "steyn"}, "word_in": "in"}}'

        self.input_series_year = 'Yuvraj Singh stats in world cup in 2011'
        self.expected_series_year = '{"player_stats": {"word_stats": "stats", "word_in": "in", "year": "2011", "series": {"series1": "world", "series2": "cup"}, "player": {"player1": "yuvraj", "player2": "singh"}}}'

        self.input_year = 'Kumar Sangakkara stats in 2011 as captain'
        self.expected_year = '{"player_stats": {"player": {"player1": "kumar", "player2": "sangakkara"}, "word_stats": "stats", "year": "2011", "word_in": "in", "word_as": "as", "word_captain": "captain"}}'

        self.input_this_year = 'Sachin Tendulkar stats in this year'
        self.expected_this_year = '{"player_stats": {"word_year": "year", "word_this_last": "this",  "word_in": "in", "word_stats": "stats", "player": {"player2": "tendulkar", "player1": "sachin"}}}'

        self.input_last_year = 'Sachin Tendulkar stats in last year'
        self.expected_last_year = '{"player_stats": {"word_year": "year", "word_this_last": "last",  "word_in": "in", "word_stats": "stats", "player": {"player2": "tendulkar", "player1": "sachin"}}}'

    def test_search_stats(self):
        self.assertParsedSentence(self.input_stats, self.expected_stats)

    def test_search_stats_captain(self):
        self.assertParsedSentence(self.input_stats_as_captain, self.expected_stats_as_captain)

    def test_search_series(self):
        self.assertParsedSentence(self.input_series, self.expected_series)

    def test_search_series_year(self):
        self.assertParsedSentence(self.input_series_year, self.expected_series_year)

    def test_search_year(self):
        self.assertParsedSentence(self.input_year, self.expected_year)

    def test_search_this_year(self):
        self.assertParsedSentence(self.input_this_year, self.expected_this_year)

    def test_search_that_year(self):
        self.assertParsedSentence(self.input_last_year, self.expected_last_year)

if __name__ == '__main__':
    unittest.main()

