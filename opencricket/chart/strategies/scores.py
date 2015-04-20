from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_scores_team = "scores -> what_is_the word_extent word_score word_of team"
    base_syntax_scores_player = "scores -> what_is_the word_extent word_score word_of player"
    return """
        %s
        %s
        %s
        %s
        what_is_the -> word_what word_is word_the
        word_what -> 'what'
        word_is -> 'is'
        word_the -> 'the'
        word_of -> 'of'
        word_score -> 'score'
        %s
        %s
        %s
        %s
         """ % (base_syntax_scores_team, base_syntax_scores_player,
                syntax_expansions.expand_with_filters(base_syntax_scores_team),
                syntax_expansions.expand_with_filters(base_syntax_scores_player),
                'nlp_player', word_config.cfg_helpers['team'],
                word_config.cfg_helpers['word_extent'],
                syntax_expansions.definition_for_expansion_filters('nlp_number'))