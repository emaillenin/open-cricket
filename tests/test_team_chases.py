import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser


class TestTeamChases(unittest.TestCase):
    def setUp(self):
        self.input = 'when was the last time india chased 300+'
        self.expected = '{"matches_cond": {"word_chased": "chased", "last_time": {"word_was": "was", "word_the": "the", "word_when": "when", "word_last": "last", "word_time": "time"}, "target": "300+", "team": {"team1": "india"}}}'

        self.input_ground = 'how many times india chased 300+ in Chennai'
        self.expected_ground = '{"matches_cond": {"team": {"team1": "india"}, "word_in": "in", "how_many_times": {"word_times": "times", "word_how": "how", "word_many": "many"}, "ground": {"ground1": "chennai"}, "word_chased": "chased", "target": "300+"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_search_gorund(self):
        parser = SentenceParser(self.input_ground)
        self.assertEqual(json.loads(self.expected_ground), json.loads(parser.parse_sentence()))


if __name__ == '__main__':
    unittest.main()

