import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache


class TestMatchesBetweenTeams(unittest.TestCase):

    def setUp(self):
        self.input = 'matches between india and england'
        self.expected = '{"matches": {"clause_between_teams": {"word_between": "between", "word_and": "and", "team_A": {"team": {"team1": "india"}}, "team_B": {"team": {"team1": "england"}}}, "word_matches": "matches"}}'

        self.input_series_year = 'matches between india and england in world cup in 2011'
        self.expected_series_year = '{"matches": {"clause_between_teams": { "word_between": "between", "word_and": "and", "team_A": {"team": {"team1": "india"}}, "team_B": {"team": {"team1": "england"}}}, "word_matches": "matches", "word_in": "in", "year": "2011", "series": {"series1": "world", "series2": "cup"}}}'

        self.input_year_match_type = 'matches between india and england in 2011 in test'
        self.expected_year_match_type = '{"matches": {"clause_between_teams": { "word_between": "between", "word_and": "and", "team_A": {"team": {"team1": "india"}}, "team_B": {"team": {"team1": "england"}}}, "word_matches": "matches", "year": "2011", "match_type" : "test", "word_in": "in"}}'

        self.input_matches_won_by_a_team = 'matches won by india'
        self.expected_matches_won_by_a_team = '{"matches": {"clause_result_by_team": {"word_won_lost": "won", "word_by": "by", "team": {"team1": "india"}}, "word_matches": "matches"}}'

        self.input_matches_played_by_a_team = 'matches played by india batting second'
        self.expected_matches_played_by_a_team = '{"matches": {"clause_batting_order": {"word_batting": "batting", "word_batting_order": "second"}, "clause_played_by_team": {"word_played": "played", "word_by": "by", "team": {"team1": "india"}}, "word_matches": "matches"}}'

        self.input_matches_won_by_a_team_against_a_team = 'matches won by india against pakistan'
        self.expected_matches_won_by_a_team_against_a_team = '{"matches": {"clause_result_against_team": {"word_won_lost": "won", "word_by": "by",  "team_A": {"team": {"team1": "india"}},  "team_B": {"team": {"team1": "pakistan"}}, "word_against": "against"}, "word_matches": "matches"}}'

        self.input_matches_won_by_a_team_batting_first = 'matches won by india batting 1st'
        self.expected_matches_won_by_a_team_batting_first = '{"matches": {"word_matches": "matches", "clause_result_by_team": {"word_won_lost": "won", "word_by": "by", "team": {"team1": "india"}}, "clause_batting_order": {"word_batting": "batting", "word_batting_order": "1st"}}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_search_series_year(self):
        parser = SentenceParser(self.input_series_year)
        self.assertEqual(json.loads(self.expected_series_year), json.loads(parser.parse_sentence()))

    def test_search_year_match_type(self):
        parser = SentenceParser(self.input_year_match_type)
        self.assertEqual(json.loads(self.expected_year_match_type), json.loads(parser.parse_sentence()))

    def test_matches_won_by_a_team(self):
        parser = SentenceParser(self.input_matches_won_by_a_team)
        self.assertEqual(json.loads(self.expected_matches_won_by_a_team), json.loads(parser.parse_sentence()))

    def test_matches_played_by_a_team(self):
        parser = SentenceParser(self.input_matches_played_by_a_team)
        self.assertEqual(json.loads(self.expected_matches_played_by_a_team), json.loads(parser.parse_sentence()))

    def test_matches_won_by_a_team_against_a_team(self):
        parser = SentenceParser(self.input_matches_won_by_a_team_against_a_team)
        self.assertEqual(json.loads(self.expected_matches_won_by_a_team_against_a_team), json.loads(parser.parse_sentence()))

    def test_matches_won_by_a_team_batting_first(self):
        parser = SentenceParser(self.input_matches_won_by_a_team_batting_first)
        self.assertEqual(json.loads(self.expected_matches_won_by_a_team_batting_first), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

