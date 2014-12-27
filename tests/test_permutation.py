import unittest

from opencricket.chart.sentence_parser import SentenceParser


class TestPermutation(unittest.TestCase):
    def test_permutation(self):
        parser = SentenceParser('')
        self.assertEqual(len(parser.permutate_filters()), 113)


if __name__ == '__main__':
    unittest.main()

