import json
from opencricket.chart.sentence_parser import SentenceParser
import unittest


class SentenceParserAssert(unittest.TestCase):
    def assertParsedSentence(self, input_search, expected_json_string):
        parser = SentenceParser(input_search)
        self.assertEqual(json.loads(expected_json_string), json.loads(parser.parse_sentence()))
