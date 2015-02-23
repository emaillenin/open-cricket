import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestPlayerStats(unittest.TestCase):

    def setUp(self):
        self.input_stats = 'Dale Steyn stats'
        self.expected_stats = '{"player_stats": {"player": {"player2": "steyn", "player1": "dale"}, "word_stats": "stats"}}'

        self.input_series = 'Dale Steyn stats in ipl'
        self.expected_series = '{"player_stats": {"word_stats": "stats", "series": {"series1": "ipl"}, "player": {"player1": "dale", "player2": "steyn"}, "word_in": "in"}}'

        self.input_series_year = 'Yuvraj Singh stats in world cup in 2011'
        self.expected_series_year = '{"player_stats": {"word_stats": "stats", "word_in": "in", "year": "2011", "series": {"series1": "world", "series2": "cup"}, "player": {"player1": "yuvraj", "player2": "singh"}}}'

        self.input_year = 'Kumar Sangakkara stats in 2011'
        self.expected_year = '{"player_stats": {"player": {"player1": "kumar", "player2": "sangakkara"}, "word_stats": "stats", "year": "2011", "word_in": "in"}}'

        self.input_this_year = 'Sachin Tendulkar stats in this year'
        self.expected_this_year = '{"player_stats": {"year": "year", "this_last": "this",  "word_in": "in", "word_stats": "stats", "player": {"player2": "tendulkar", "player1": "sachin"}}}'

        self.input_last_year = 'Sachin Tendulkar stats in last year'
        self.expected_last_year = '{"player_stats": {"year": "year", "this_last": "last",  "word_in": "in", "word_stats": "stats", "player": {"player2": "tendulkar", "player1": "sachin"}}}'

    def test_search_stats(self):
        parser = SentenceParser(self.input_stats)
        self.assertEqual(json.loads(self.expected_stats), json.loads(parser.parse_sentence()))

    def test_search_series(self):
        parser = SentenceParser(self.input_series)
        self.assertEqual(json.loads(self.expected_series), json.loads(parser.parse_sentence()))

    def test_search_series_year(self):
        parser = SentenceParser(self.input_series_year)
        self.assertEqual(json.loads(self.expected_series_year), json.loads(parser.parse_sentence()))

    def test_search_year(self):
        parser = SentenceParser(self.input_year)
        self.assertEqual(json.loads(self.expected_year), json.loads(parser.parse_sentence()))

    def test_search_this_year(self):
        parser = SentenceParser(self.input_this_year)
        self.assertEqual(json.loads(self.expected_this_year), json.loads(parser.parse_sentence()))

    def test_search_that_year(self):
        parser = SentenceParser(self.input_last_year)
        self.assertEqual(json.loads(self.expected_last_year), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

