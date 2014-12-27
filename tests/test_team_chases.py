import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser


class TestTeamChases(unittest.TestCase):
    def setUp(self):
        self.input = 'when was the last time india chased down 300+ successfully'
        self.expected = '{"matches_cond": {"chased_s": {"down": "down", "chased": "chased"}, "filler": "successfully", "what": {"last_time": {"was": "was", "the": "the", "when": "when", "last": "last", "time": "time"}}, "score": "300+", "team": {"team1": "india"}}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))


if __name__ == '__main__':
    unittest.main()

