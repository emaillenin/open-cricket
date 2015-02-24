import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser


class TestTeamChases(unittest.TestCase):
    def setUp(self):
        self.input = 'when was the last time india chased down 300+'
        self.expected = '{"matches_cond": {"chased_s": {"down": "down", "chased": "chased"}, "what": {"last_time": {"was": "was", "the": "the", "when": "when", "last": "last", "time": "time"}}, "score": "300+", "team": {"team1": "india"}}}'

        self.input_ground = 'how many times india chased down 300+ in Chennai'
        self.expected_ground = '{"matches_cond": {"word_in": "in", "team": {"team1": "india"}, "what": {"how_many_times": {"times": "times", "how": "how", "many": "many"}}, "ground": {"ground1": "chennai"}, "chased_s": {"down": "down", "chased": "chased"}, "score": "300+"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_search_gorund(self):
        parser = SentenceParser(self.input_ground)
        self.assertEqual(json.loads(self.expected_ground), json.loads(parser.parse_sentence()))


if __name__ == '__main__':
    unittest.main()

