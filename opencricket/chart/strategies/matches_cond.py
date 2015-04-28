from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_matches_cond_last_time = 'matches_cond -> last_time team word_chased target'
    base_syntax_matches_cond_how_many_times = 'matches_cond -> how_many_times team word_chased target'
    return """
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        %s
        word_chased -> 'chased'
        %s
        """ % (base_syntax_matches_cond_last_time, base_syntax_matches_cond_how_many_times,
               syntax_expansions.expand_with_filters(base_syntax_matches_cond_how_many_times),
               syntax_expansions.expand_with_filters(base_syntax_matches_cond_last_time),
               syntax_expansions.definition_for_expansion_filters('nlp_number'),
               word_config.cfg_helpers['last_time'], word_config.cfg_helpers['how_many_times'], word_config.cfg_helpers['team'],
               word_config.cfg_helpers['target'])