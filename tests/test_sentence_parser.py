import unittest

from nltk import Tree

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_cache import SyntaxCache


class TestSentenceParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SyntaxCache().build_cache()

    def setUp(self):
        self.input_tree = Tree.fromstring(
            "(matches (word_matches matches) (word_played played) (word_by by) (team sri lanka))")
        self.expected_dict = {'team': 'sri lanka', 'word_by': 'by', 'word_matches': 'matches', 'word_played': 'played'}

    def test_tree_to_dict(self):
        parser = SentenceParser('dummy')
        result_dict = parser.tree_to_dict(self.input_tree)
        self.assertEqual(self.expected_dict, result_dict)


if __name__ == '__main__':
    unittest.main()
