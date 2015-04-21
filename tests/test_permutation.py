import unittest

from opencricket.chart import syntax_expansions


class TestPermutation(unittest.TestCase):
    def test_permutation(self):
        self.assertEqual(len(syntax_expansions.permutate_filters(['match_type', 'series', 'word_in year', 'ground'])), 65)

    def test_should_only_permutate_upto_3_filter_items(self):
        self.assertEqual(len(syntax_expansions.permutate_filters(['match_type', 'series', 'word_in year', 'ground', 'clause_between_teams', 'clause_result_by_team'])), 227)


if __name__ == '__main__':
    unittest.main()

