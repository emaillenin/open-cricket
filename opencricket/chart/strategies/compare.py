from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_compare = 'compare -> word_compare clause_player'
    return """
        %s
        %s
        %s
        clause_player -> elite-player_1 word_and elite-player_2
        elite-player_1 -> player
        elite-player_2 -> player
        word_compare -> 'compare'
        %s
        %s
        """ % (base_syntax_compare, syntax_expansions.expand_with_filters(base_syntax_compare),
               syntax_expansions.definition_for_expansion_filters('nlp_number'),
               'nlp_player',
               word_config.cfg_helpers['word_and'])