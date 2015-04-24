import itertools
from opencricket.config import word_config


def expand_with_filters(base_syntax):
    final_syntax = ''
    for f in permutate_filters(word_config.expandable_filters_in):
        final_syntax += """%s %s\n""" % (base_syntax, ' '.join(f))
    return final_syntax


def expand_with_matches_clauses(base_syntax):
    final_syntax = ''
    for f in permutate_filters(word_config.expandable_match_clauses + word_config.expandable_filters_in):
        final_syntax += """%s %s\n""" % (base_syntax, ' '.join(f))
    final_syntax += """
                          %s
                          %s
                          %s
                          %s
                          %s
                          %s
                          %s
                          %s
                          wickets -> %s
                    """ % (
        build_syntax_with_expandable_filters('clause_result_by_team',
                                             word_config.match_clauses['clause_result_by_team']),
        build_syntax_with_expandable_filters('clause_between_teams',
                                             word_config.match_clauses['clause_between_teams']),
        build_syntax_with_expandable_filters('clause_result_against_team',
                                             word_config.match_clauses['clause_result_against_team']),
        build_syntax_with_expandable_filters('clause_batting_order',
                                             word_config.match_clauses['clause_batting_order']),
        build_syntax_with_expandable_filters('clause_played_by_team',
                                             word_config.match_clauses['clause_played_by_team']),
        word_config.cfg_helpers['word_won_lost'],
        word_config.cfg_helpers['word_between'],
        word_config.cfg_helpers['word_by'],
        'nlp_number')

    return final_syntax


def definition_for_expansion_filters(year):
    return """
        %s
        %s
        %s
        %s
        %s
        %s
        year -> %s
        """ % (
        'nlp_ground',
        word_config.cfg_helpers['word_this_last'],
        word_config.cfg_helpers['word_in'],
        word_config.cfg_helpers['word_year'],
        word_config.cfg_helpers['series'],
        word_config.cfg_helpers['in_match_type'],
        year)

def replace_nlp_placeholders(syntax):
    for r in ['nlp_player', 'nlp_ground', 'nlp_number']:
        syntax = syntax.replace(r, word_config.cfg_helpers[r])
    return syntax

def permutate_filters(filters):
    permutated_filters = []
    # It's okay to expand only upto 3 filter clauses. no question will have more than that
    for i in range(1, min(len(filters) + 1, 4)):
        for f in itertools.permutations(filters, i):
            permutated_filters += [list(f)]
            if 'word_in year' in f:
                this_last_year_list = list(f)
                this_last_year_list[this_last_year_list.index('word_in year')] = 'word_in word_this_last word_year'
                permutated_filters += [this_last_year_list]
    return permutated_filters


def build_syntax_with_expandable_filters(key, value):
    # You should not be accessing __class__. Does python have .is_a?
    if value.__class__.__name__ == 'str':
        value = [value]
    return '\n'.join(list(key + ' -> ' + v for v in value))