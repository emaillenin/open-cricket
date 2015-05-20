import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserHelper


class TestMatchesAndClauses(SentenceParserHelper):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input_matches_won_by_a_team = 'matches won by india'
        self.expected_matches_won_by_a_team = '{"matches": {"clause_result_by_team": {"word_won_lost": "won", "word_by": "by", "team": {"team1": "india"}}, "word_matches": "matches"}}'

        self.input_matches_played_by_a_team = 'matches played by india batting second in 2011'
        self.expected_matches_played_by_a_team = '{"matches": {"word_in": "in", "year": "2011", "clause_batting_order": {"word_batting": "batting", "word_batting_order": "second"}, "clause_result_by_team": {"word_played": "played", "word_by": "by", "team": {"team1": "india"}}, "word_matches": "matches"}}'

        self.input_matches_played_by_two_teams = 'matches played by india and sri lanka'
        self.expected_matches_played_by_two_teams = '{"matches": {"clause_result_by_team": {"word_played": "played", "team_B": {"team": {"team2": "lanka", "team1": "sri"}}, "word_by": "by", "word_and": "and", "team_A": {"team": {"team1": "india"}}}, "word_matches": "matches"}}'

        self.input_matches_won_by_a_team_against_a_team = 'matches won by india against pakistan in world cup'
        self.expected_matches_won_by_a_team_against_a_team = '{"matches": {"word_in": "in", "series": {"series1": "world", "series2": "cup"}, "clause_result_by_team": {"word_won_lost": "won", "word_by": "by",  "team_A": {"team": {"team1": "india"}},  "team_B": {"team": {"team1": "pakistan"}}, "word_against": "against"}, "word_matches": "matches"}}'

        self.input_matches_won_by_a_team_batting_first = 'matches won by india batting 1st in odi'
        self.expected_matches_won_by_a_team_batting_first = '{"matches": {"word_matches": "matches", "match_type" : "odi", "word_in": "in", "clause_result_by_team": {"word_won_lost": "won", "word_by": "by", "team": {"team1": "india"}}, "clause_batting_order": {"word_batting": "batting", "word_batting_order": "1st"}}}'

        self.input_matches_won_by_a_team_innings_score = 'matches won by india scoring 300'
        self.expected_matches_won_by_a_team_innings_score = '{"matches": {"word_matches": "matches", "clause_result_by_team": {"word_won_lost": "won", "word_by": "by", "team": {"team1": "india"}}, "clause_innings_score": {"word_scoring": "scoring", "innings_score": "300"}}}'

        self.input_matches_lost_by_a_team_while_chasing = 'matches lost by india chasing 100'
        self.expected_matches_lost_by_a_team_while_chasing = '{"matches": {"word_matches": "matches", "clause_result_by_team": {"word_won_lost": "lost", "word_by": "by", "team": {"team1": "india"}}, "clause_chasing_score": {"word_chasing": "chasing", "target": "100"}}}'

        self.input_matches_won_by_a_team_with_wickets_left = 'matches won by india chasing 300 with 5 wickets left in odi'
        self.expected_matches_won_by_a_team_with_wickets_left = '{"matches": {"match_type": "odi", "word_in": "in", "clause_wickets_left": {"wickets": "5", "word_wickets": "wickets", "word_with": "with", "word_left": "left"}, "clause_chasing_score": {"target": "300", "word_chasing": "chasing"}, "word_matches": "matches", "clause_result_by_team": {"word_won_lost": "won", "team": {"team1": "india"}, "word_by": "by"}}}'

    def test_matches_won_by_a_team(self):
        self.assertParsedSentence(self.input_matches_won_by_a_team, self.expected_matches_won_by_a_team)

    def test_matches_played_by_a_team(self):
        self.assertParsedSentence(self.input_matches_played_by_a_team, self.expected_matches_played_by_a_team)

    def test_matches_played_by_two_teams(self):
        self.assertParsedSentence(self.input_matches_played_by_two_teams, self.expected_matches_played_by_two_teams)

    def test_matches_won_by_a_team_against_a_team(self):
        self.assertParsedSentence(self.input_matches_won_by_a_team_against_a_team,
                                  self.expected_matches_won_by_a_team_against_a_team)

    def test_matches_won_by_a_team_batting_first(self):
        self.assertParsedSentence(self.input_matches_won_by_a_team_batting_first,
                                  self.expected_matches_won_by_a_team_batting_first)

    def test_matches_won_by_a_team_with_a_min_score(self):
        self.assertParsedSentence(self.input_matches_won_by_a_team_innings_score,
                                  self.expected_matches_won_by_a_team_innings_score)

    def test_matches_lost_by_a_team_while_chasing(self):
        self.assertParsedSentence(self.input_matches_lost_by_a_team_while_chasing,
                                  self.expected_matches_lost_by_a_team_while_chasing)

    def test_matches_won_by_a_team_with_wickets_left(self):
        self.assertParsedSentence(self.input_matches_won_by_a_team_with_wickets_left,
                                  self.expected_matches_won_by_a_team_with_wickets_left)

if __name__ == '__main__':
    unittest.main()

