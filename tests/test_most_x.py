import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser


class TestMostX(unittest.TestCase):

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
        self.expected_team_player = '{"most_x": {"ground": {"ground1": "australia"}, "metric": {"metric1": "runs" }, "word_in": "in", "series": {"series2": "cup", "series1": "world"}, "word_most": "most", "word_the": "the", "word_has": "has",  "who_player": {"word_player": "player", "word_which": "which", "team_player": {"team_player1": "indian"}}}}'

    def test_search_sixes(self):
        parser = SentenceParser(self.input_sixes)
        self.assertEqual(json.loads(self.expected_sixes), json.loads(parser.parse_sentence()))

    def test_search_not_outs(self):
        parser = SentenceParser(self.input_not_outs)
        self.assertEqual(json.loads(self.expected_not_outs), json.loads(parser.parse_sentence()))

    def test_search_bowling_strike_rate(self):
        parser = SentenceParser(self.input_bowling_strike_rate)
        self.assertEqual(json.loads(self.expected_bowling_strike_rate), json.loads(parser.parse_sentence()))

    def test_search_match_type(self):
        parser = SentenceParser(self.input_match_type)
        self.assertEqual(json.loads(self.expected_match_type), json.loads(parser.parse_sentence()))

    def test_search_which_player(self):
        parser = SentenceParser(self.input_which_player)
        self.assertEqual(json.loads(self.expected_which_player), json.loads(parser.parse_sentence()))

    def test_search_ground(self):
        parser = SentenceParser(self.input_ground)
        self.assertEqual(json.loads(self.expected_ground), json.loads(parser.parse_sentence()))

    def test_search_series_year(self):
        parser = SentenceParser(self.input_series_year)
        self.assertEqual(json.loads(self.expected_series_year), json.loads(parser.parse_sentence()))

    def test_search_match_type_year(self):
        parser = SentenceParser(self.input_match_type_year)
        self.assertEqual(json.loads(self.expected_match_type_year), json.loads(parser.parse_sentence()))

    def test_year_match_type(self):
        parser = SentenceParser(self.input_year_match_type)
        self.assertEqual(json.loads(self.expected_year_match_type), json.loads(parser.parse_sentence()))

    def test_team_player(self):
        parser = SentenceParser(self.input_team_player )
        self.assertEqual(json.loads(self.expected_team_player), json.loads(parser.parse_sentence()))

if __name__ == '__main__':
    unittest.main()

