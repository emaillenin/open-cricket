from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_player_stats = """player_stats -> player word_stats"""
    return """
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        word_stats -> 'stats'
        """ % (
        base_syntax_player_stats,
        syntax_expansions.expand_with_filters(base_syntax_player_stats,
                                          ['word_as word_captain',
                                           'word_batting word_wkt_order',
                                           'word_as words_wicket_keeper',
                                           'word_against team']),
        word_config.cfg_helpers['word_as'],
        word_config.cfg_helpers['team'],
        word_config.cfg_helpers['word_against'],
        word_config.cfg_helpers['word_captain'],
        word_config.cfg_helpers['words_wicket_keeper'],
        word_config.cfg_helpers['word_batting'],
        word_config.cfg_helpers['word_wkt_order'],
        syntax_expansions.definition_for_expansion_filters('nlp_number'),
        'nlp_player')
