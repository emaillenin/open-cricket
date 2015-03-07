import unittest
import json

from opencricket.chart.syntax_response import SyntaxResponse

class TestSyntaxResponse(unittest.TestCase):

    def setUp(self):
        self.syntax_string = '{"compare": {"player_1": {"player": {"player1": "sehwag"}}, "player_2": {"player": {"player1": "dhoni"}}, "CC": "and", "compare_word": "compare"}}'
        self.response_string = '{"root": "compare", "compare": {"compare_word": "compare", "player_2": {"player": {"player1": "dhoni"}}, "CC": "and", "player_1": {"player": {"player1": "sehwag"}}}, "suggested": false}'

    def test_syntax_response_false_suggestion(self):
        response_dict = SyntaxResponse.build_response(self.syntax_string, False)
        self.assertEqual(json.loads(self.response_string), response_dict)

if __name__ == '__main__':
    unittest.main()

