from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_matches = """matches -> word_matches"""
    return """
        %s
        %s
        %s
        %s
        word_matches -> 'matches'
        team_A -> team
        team_B -> team
        %s
        %s
        %s
        %s
        %s
        %s
        """ % (base_syntax_matches, syntax_expansions.expand_with_filters(base_syntax_matches),
               syntax_expansions.definition_for_expansion_filters('nlp_number'),
               syntax_expansions.expand_with_matches_clauses(base_syntax_matches),
               word_config.cfg_helpers['team'],
               word_config.cfg_helpers['word_against'],
               word_config.cfg_helpers['word_batting_order'],
               word_config.cfg_helpers['word_batting'],
               word_config.cfg_helpers['word_played'],
               word_config.cfg_helpers['word_and'])
