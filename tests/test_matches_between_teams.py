import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestMatchesBetweenTeams(unittest.TestCase):

    def setUp(self):
        self.input = 'matches between india and england'
        self.expected = '{"matches": {"clause": {"CC": "and", "teamA": {"team": {"team1": "india"}}, "teamB": {"team": {"team1": "england"}}}, "select": "matches", "IN": "between"}}'

        self.input_series_year = 'matches between india and england in world cup 2011'
        self.expected_series_year = '{"matches": {"clause": {"CC": "and", "teamA": {"team": {"team1": "india"}}, "teamB": {"team": {"team1": "england"}}}, "select": "matches", "IN": "between", "filler": "in", "year": "2011", "series": {"series1": "world", "series2": "cup"}}}'
        
        self.input_year_match_type = 'matches between india and england in 2011 in test'
        self.expected_year_match_type = '{"matches": {"clause": {"CC": "and", "teamA": {"team": {"team1": "india"}}, "teamB": {"team": {"team1": "england"}}}, "select": "matches", "IN": "between", "year": "2011", "match_type" : "test", "filler": "in"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_search_series_year(self):
        parser = SentenceParser(self.input_series_year)
        self.assertEqual(json.loads(self.expected_series_year), json.loads(parser.parse_sentence()))

    def test_search_year_match_type(self):
        parser = SentenceParser(self.input_year_match_type)
        self.assertEqual(json.loads(self.expected_year_match_type), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

