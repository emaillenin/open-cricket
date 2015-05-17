import glob
import os
from os.path import basename
import unittest
import json

from opencricket.suggestion.productions import Productions


class TestProductions(unittest.TestCase):
    def setUp(self):
        self.expansions = {
            "word_in": "in",
            "word_year": "year",
            "word_by": "by",
            "word_between": "between",
            "word_with": "with",
            "word_matches": "matches",
            "word_batting": "batting",
            "word_left": "left",
            "word_scoring": "scoring",
            "word_against": "against",
            "word_and": "and",
            "word_played": "played",
            "word_wickets": "wickets",
            "word_chasing": "chasing"
        }

        self.dynamic_expansions = {
            "clause_innings_score": [
                "word_scoring innings_score"
            ],
            "clause_wickets_left": [
                "word_with wickets word_wickets word_left"
            ],
            "clause_batting_order": [
                "word_batting word_batting_order"
            ],
            "clause_result_by_team": [
                "word_won_lost word_by team",
                "word_played word_by team",
                "word_played word_by team_A word_and team_B",
                "word_won_lost word_by team_A word_against team_B"
            ],
            "clause_chasing_score": [
                "word_chasing target"
            ]
        }

        self.syntax = [
            "word_matches",
            "word_matches word_in match_type",
            "word_matches word_in series",
            "word_matches word_in year",
            "word_matches word_in word_this_last word_year",
            "word_matches word_in ground",
            "word_matches word_in match_type word_in series",
            "word_matches word_in match_type word_in year",
            "word_matches word_in match_type word_in word_this_last word_year",
            "word_matches word_in match_type word_in ground",
            "word_matches word_in series word_in year",
            "word_matches word_in series word_in word_this_last word_year",
            "word_matches word_in series word_in ground",
            "word_matches word_in year word_in ground",
            "word_matches word_in word_this_last word_year word_in ground",
            "word_matches clause_batting_order",
            "word_matches clause_wickets_left",
            "word_matches clause_innings_score",
            "word_matches clause_result_by_team",
            "word_matches clause_chasing_score",
            "word_matches clause_batting_order clause_wickets_left",
            "word_matches clause_batting_order clause_innings_score",
            "word_matches clause_batting_order clause_result_by_team",
            "word_matches clause_batting_order clause_chasing_score",
            "word_matches clause_batting_order word_in match_type",
            "word_matches clause_batting_order word_in series",
            "word_matches clause_batting_order word_in year",
            "word_matches clause_batting_order word_in word_this_last word_year",
            "word_matches clause_batting_order word_in ground",
            "word_matches clause_wickets_left clause_innings_score",
            "word_matches clause_wickets_left clause_result_by_team",
            "word_matches clause_wickets_left clause_chasing_score",
            "word_matches clause_wickets_left word_in match_type",
            "word_matches clause_wickets_left word_in series",
            "word_matches clause_wickets_left word_in year",
            "word_matches clause_wickets_left word_in word_this_last word_year",
            "word_matches clause_wickets_left word_in ground",
            "word_matches clause_innings_score clause_result_by_team",
            "word_matches clause_innings_score clause_chasing_score",
            "word_matches clause_innings_score word_in match_type",
            "word_matches clause_innings_score word_in series",
            "word_matches clause_innings_score word_in year",
            "word_matches clause_innings_score word_in word_this_last word_year",
            "word_matches clause_innings_score word_in ground",
            "word_matches clause_result_by_team clause_chasing_score",
            "word_matches clause_result_by_team word_in match_type",
            "word_matches clause_result_by_team word_in series",
            "word_matches clause_result_by_team word_in year",
            "word_matches clause_result_by_team word_in word_this_last word_year",
            "word_matches clause_result_by_team word_in ground",
            "word_matches clause_chasing_score word_in match_type",
            "word_matches clause_chasing_score word_in series",
            "word_matches clause_chasing_score word_in year",
            "word_matches clause_chasing_score word_in word_this_last word_year",
            "word_matches clause_chasing_score word_in ground"
        ]

    def test_productions(self):
        expansions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'expansions')
        productions = Productions().productions(expansions_path)

        self.assertEqual(8, len(productions))

        matches_productions = productions[1]['matches']

        # Remove keys that get random words everytime (1st, 2nd etc). Should fix this, to get reproducible results.
        matches_productions['expansions'].pop('word_batting_order')
        matches_productions['expansions'].pop('word_won_lost')
        matches_productions['expansions'].pop('word_this_last')

        self.assertEqual(matches_productions['syntax'], self.syntax)
        self.assertEqual(matches_productions['expansions'], self.expansions)
        self.assertEqual(matches_productions['dynamic_expansions'], self.dynamic_expansions)

    def test_explode(self):
        expansions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'expansions')
        exploded_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'exploded')

        Productions().explode(expansions_path, exploded_path)

        self.assertEqual(list(map(basename, glob.iglob(os.path.join(exploded_path, '*')))),
                         ['compare', 'matches', 'matches_cond', 'most_x', 'partnerships', 'player_dismissals',
                          'player_stats', 'scores'])


if __name__ == '__main__':
    unittest.main()

