import unittest
from elasticsearch import Elasticsearch

class TestElasticSearch(unittest.TestCase):

    def test_elasticsearch(self):
        es = Elasticsearch()
        self.assertEqual(es.ping(), False)

if __name__ == '__main__':
    unittest.main()

