import itertools
from opencricket.config import word_config


def expand_with_filters(base_syntax):
    final_syntax = ''
    for f in permutate_filters(word_config.expandable_filters_in):
        final_syntax += """
                            %s %s
                        """ % (base_syntax, ' '.join(f))
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
        word_config.cfg_helpers['ground'],
        word_config.cfg_helpers['word_this_last'],
        word_config.cfg_helpers['word_in'],
        word_config.cfg_helpers['word_year'],
        word_config.cfg_helpers['series'],
        word_config.cfg_helpers['in_match_type'],
        year)

def permutate_filters(filters):
    permutated_filters = []
    for i in range(1, min(len(filters) + 1, 5)):
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