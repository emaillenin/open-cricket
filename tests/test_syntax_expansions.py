from unittest import TestCase
from opencricket.chart import syntax_expansions


class TestSyntaxExpansions(TestCase):
    def setUp(self):
        self.expected_syntax = 'clause_result_by_team -> word_won word_by team'
        self.expected_syntax_array = 'clause_result_by_team -> word_won word_by team\n' \
                                     'clause_result_by_team -> word_lost word_by team'

    def test_build_syntax_array(self):
        result_syntax = syntax_expansions.build_syntax_with_expandable_filters('clause_result_by_team',
                                                 ['word_won word_by team', 'word_lost word_by team'])
        self.assertEqual(self.expected_syntax_array, result_syntax)

    def test_build_syntax_item(self):
        result_syntax = syntax_expansions.build_syntax_with_expandable_filters('clause_result_by_team', 'word_won word_by team')
        self.assertEqual(self.expected_syntax, result_syntax)