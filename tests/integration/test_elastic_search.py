import unittest
import json

import elasticsearch
from elasticsearch import helpers

from environment import Test
import flaskr
from opencricket.config import es_config
from opencricket.suggestion.productions import Productions, OPEN_CRICKET_INDEX


def seed_elastic_search():
    test_es_connection = es_config.es_builder(port=Test.ELASTICSEARCH_PORT)
    test_productions = Productions(test_es_connection)
    test_productions.delete_index()
    test_productions.create_index()
    seeds = ['Who has the best bowling figure in Australia', 'Who has the best bowling figure in India',
             'Who has the best bowling average in Australia']
    actions = list({
                       "_index": OPEN_CRICKET_INDEX,
                       "_type": 'most_x',
                       "_source": {
                           "question": line.strip()
                       }} for line in seeds)
    elasticsearch.helpers.bulk(test_es_connection, actions, chunk_size=100)


class TestElasticSearch(unittest.TestCase):
    def setUp(self):
        self.app = flaskr.app.test_client()
        # seed_elastic_search()
        self.expected_best_bowling_figure = json.loads('{"suggested": true, '
                                                       '"suggested_search": "Who has the best bowling figure in Australia", '
                                                       '"root": "most_x", '
                                                       '"most_x": {"word_against": "against", "word_has": "has", "word_most": "most", "word_the": "the", "metric": "bowling figure", "who_player": {"word_who": "who"}, "team": "australia"}'
                                                       '}')

    # Parking this test since we cannot start Elasticsearch in 9300 within a test
    def ignore_suggestion_from_elastic_search(self):
        # Should suggest Ground names capitalized
        rv = self.app.get('/?search=Who has the best bowling figure in australia?')
        self.assertEqual(rv._status_code, 200)
        print(rv.data.decode("utf-8"))
        self.assertEqual(json.loads(rv.data.decode("utf-8")), self.expected_best_bowling_figure)


if __name__ == '__main__':
    unittest.main()
