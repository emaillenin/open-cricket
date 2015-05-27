import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache
from tests.support.sentence_parser_helper import SentenceParserAssert


class TestMostX(SentenceParserAssert):

    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input_sixes = 'who has the most sixes'
        self.expected_sixes = '{"most_x": {"word_most": "most", "who_player": {"word_who": "who"}, "metric": {"metric1": "sixes" }, "word_the": "the", "word_has": "has"}}'

        self.input_not_outs = 'who has the highest not outs'
        self.expected_not_outs = '{"most_x": {"word_most": "highest", "who_player": {"word_who": "who"}, "metric": {"metric1": "not", "metric2": "outs" }, "word_the": "the", "word_has": "has"}}'

        self.input_bowling_strike_rate = 'who has the best bowling strike rate'
        self.expected_bowling_strike_rate = '{"most_x": {"word_most": "best", "who_player": {"word_who": "who"}, "metric": {"metric1": "bowling", "metric2": "strike", "metric3": "rate" }, "word_the": "the", "word_has": "has"}}'

        self.input_match_type = 'who has the most fours in ODI'
        self.expected_match_type = '{"most_x": {"word_the": "the", "word_has": "has", "word_in": "in", "match_type": "odi", "who_player": {"word_who": "who"}, "metric": {"metric1": "fours" }, "word_most": "most"}}'

        self.input_which_player = 'which player has the most sixes'
        self.expected_which_player = '{"most_x": {"word_the": "the", "word_has": "has",  "who_player": {"word_player": "player", "word_which": "which"}, "word_most": "most", "metric": {"metric1": "sixes" }}}'

        self.input_which_captain = 'which south african captain has the most sixes'
        self.expected_which_captain = '{"most_x": {"word_the": "the", "word_has": "has", "who_player": {"word_captain": "captain", "word_which": "which", "teamplayer": {"team_player1": "south", "team_player2": "african"}}, "word_most": "most", "metric": {"metric1": "sixes" }}}'

        self.input_ground = 'which player has the most sixes in Chennai'
        self.expected_ground = '{"most_x": {"word_the": "the", "word_has": "has", "word_in": "in", "who_player": {"word_player": "player", "word_which": "which"}, "word_most": "most", "metric": {"metric1": "sixes" }, "ground": {"ground1": "chennai"}}}'

        # Title case not to be detected as Ground
        self.input_series_year = 'which player has the most sixes in World Cup in 2011'
        self.expected_series_year = '{"most_x": {"metric": {"metric1": "sixes" }, "word_the": "the", "word_has": "has", "word_in": "in", "series": {"series2": "cup", "series1": "world"}, "word_most": "most", "year": "2011", "who_player": {"word_player": "player", "word_which": "which"}}}'

        self.input_match_type_year = 'which player has the most runs in 2011 in test'
        self.expected_match_type_year = '{"most_x": {"year": "2011", "metric": {"metric1": "runs" }, "word_in": "in", "match_type": "test", "word_most": "most", "word_the": "the", "word_has": "has", "who_player": {"word_player": "player", "word_which": "which"}}}'

        self.input_year_match_type = 'who has the most runs in t20 in 2014'
        self.expected_year_match_type = '{"most_x": {"year": "2014", "metric": {"metric1": "runs" }, "word_in": "in", "match_type": "t20", "word_most": "most", "word_the": "the", "word_has": "has", "who_player": {"word_who": "who"}}}'

        self.input_team_player = 'which Indian player has the most runs in World Cup in Australia'
        self.expected_team_player = '{"most_x": {"ground": {"ground1": "australia"}, "metric": {"metric1": "runs" }, "word_in": "in", "series": {"series2": "cup", "series1": "world"}, "word_most": "most", "word_the": "the", "word_has": "has",  "who_player": {"word_player": "player", "word_which": "which", "teamplayer": {"team_player1": "indian"}}}}'

        self.input_against_team = 'which player has the most sixes against India'
        self.expected_against_team = '{"most_x": {"word_the": "the", "word_has": "has",  "who_player": {"word_player": "player", "word_which": "which"}, "word_most": "most", "metric": {"metric1": "sixes" },  "word_against": "against", "team": {"team1": "india"}}}'

    def test_search_sixes(self):
        self.assertParsedSentence(self.input_sixes, self.expected_sixes)

    def test_search_not_outs(self):
        self.assertParsedSentence(self.input_not_outs, self.expected_not_outs)

    def test_search_bowling_strike_rate(self):
        self.assertParsedSentence(self.input_bowling_strike_rate, self.expected_bowling_strike_rate)

    def test_search_match_type(self):
        self.assertParsedSentence(self.input_match_type, self.expected_match_type)

    def test_search_which_player(self):
        self.assertParsedSentence(self.input_which_player, self.expected_which_player)

    def test_search_which_captain(self):
        self.assertParsedSentence(self.input_which_captain, self.expected_which_captain)

    def test_search_ground(self):
        self.assertParsedSentence(self.input_ground, self.expected_ground)

    def test_search_series_year(self):
        self.assertParsedSentence(self.input_series_year, self.expected_series_year)

    def test_search_match_type_year(self):
        self.assertParsedSentence(self.input_match_type_year, self.expected_match_type_year)

    def test_year_match_type(self):
        self.assertParsedSentence(self.input_year_match_type, self.expected_year_match_type)

    def test_team_player(self):
        self.assertParsedSentence(self.input_team_player, self.expected_team_player)

    def test_against_team(self):
        self.assertParsedSentence(self.input_against_team, self.expected_against_team)

if __name__ == '__main__':
    unittest.main()

