from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_dismissals_with_team = 'player_dismissals -> word_dismissals word_by dismissals word_in team'
    base_syntax_dismissals = 'player_dismissals -> word_dismissals word_by dismissals'
    return """
        %s
        %s
        %s
        %s
        word_dismissals -> 'dismissals'
        %s
        %s
        %s
        word_in -> 'in'
        word_by -> 'by'
        """ % (base_syntax_dismissals_with_team, base_syntax_dismissals,
               syntax_expansions.expand_with_filters(base_syntax_dismissals_with_team),
               syntax_expansions.expand_with_filters(base_syntax_dismissals),
               syntax_expansions.definition_for_expansion_filters('nlp_number'),
               word_config.cfg_helpers['team'],
               word_config.cfg_helpers['dismissals'])