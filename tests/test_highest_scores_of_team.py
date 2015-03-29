import unittest
import json

from opencricket.chart.sentence_parser import SentenceParser

class TestHighestTeamScore(unittest.TestCase):

    def setUp(self):
        self.input = "what is the highest score of england"
        self.expected = '{"scores": {"team": {"team1": "england"}, "what_is_the": {"word_is": "is", "word_what": "what", "word_the": "the"}, "word_score": "score", "word_extent": "highest", "word_of": "of"}}'

        self.input_in_this_year = "what is the highest score of england in this year"
        self.expected_in_this_year = '{"scores": {"word_year": "year", "word_this_last": "this", "word_in": "in", "team": {"team1": "england"}, "what_is_the": {"word_is": "is", "word_what": "what", "word_the": "the"}, "word_score": "score", "word_extent": "highest", "word_of": "of"}}'

    def test_search(self):
        parser = SentenceParser(self.input)
        self.assertEqual(json.loads(self.expected), json.loads(parser.parse_sentence()))

    def test_search_in_this_year(self):
        parser = SentenceParser(self.input_in_this_year)
        self.assertEqual(json.loads(self.expected_in_this_year), json.loads(parser.parse_sentence()))

if __name__ == "__main__":
    unittest.main()

