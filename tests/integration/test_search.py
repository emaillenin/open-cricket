import unittest
import json
import flaskr


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.app = flaskr.app.test_client()
        self.expected_response = json.loads('{"suggested": false, "root": "player_stats", "player_stats": {"word_stats": "stats", "player": {"player1": "virat", "player2": "kohli"}}}')

    def test_search(self):
        rv = self.app.get('/?search=Virat Kohli Stats')
        self.assertEqual(rv._status_code, 200)
        self.assertEqual(json.loads(rv.data.decode("utf-8")), self.expected_response)

if __name__ == '__main__':
    unittest.main()

