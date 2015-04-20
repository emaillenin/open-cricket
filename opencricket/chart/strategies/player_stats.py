from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_player_stats = """player_stats -> player word_stats"""
    return """
        %s
        %s
        %s
        %s
        word_stats -> 'stats'
        """ % (
        base_syntax_player_stats,
        syntax_expansions.expand_with_filters(base_syntax_player_stats),
        syntax_expansions.definition_for_expansion_filters('nlp_number'),
        'nlp_player')
