import unittest

from opencricket.config import word_config


class TestWordConfig(unittest.TestCase):

    def setUp(self):
        self.teams_list = ['india', 'chennai super kings', 'sri lanka', 'west indies']
        self.teams_split = ["'india'", "'chennai' 'super' 'kings'", "'sri' 'lanka'", "'west' 'indies'"]
        self.expected_pipe_syntax = "'india' | 'chennai' 'super' 'kings' | 'sri' 'lanka' | 'west' 'indies'"

    def test_build_syntax_multi_word(self):
        self.assertEqual(word_config.form_multi_word_config(self.teams_list), self.teams_split)

    def test_pipe_syntax(self):
        self.assertEqual(word_config.join_for_pipe_config(self.teams_split), self.expected_pipe_syntax)

if __name__ == '__main__':
    unittest.main()

