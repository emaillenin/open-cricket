from opencricket.config import word_config
from opencricket.chart import syntax_expansions


def syntax():
    base_syntax_part1 = 'partnerships -> word_extent word_partnership'
    base_syntax_part2 = 'partnerships -> word_extent word_partnership word_for word_wkt_order word_wicket'
    base_syntax_part3 = 'partnerships -> word_extent word_partnership word_for team'
    base_syntax_part4 = 'partnerships -> word_extent word_partnership word_for word_wkt_order word_wicket word_for team'
    base_syntax_part5 = 'partnerships -> word_extent word_partnership word_for team word_for word_wkt_order word_wicket'
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
        word_partnership -> 'partnership'
        %s
        %s
        %s
        %s
        word_for -> 'for'
        word_wicket -> 'wicket'
        """ % (base_syntax_part1, base_syntax_part2, base_syntax_part3, base_syntax_part4, base_syntax_part5,
               syntax_expansions.expand_with_filters(base_syntax_part1),
               syntax_expansions.expand_with_filters(base_syntax_part2),
               syntax_expansions.expand_with_filters(base_syntax_part3),
               syntax_expansions.expand_with_filters(base_syntax_part4),
               syntax_expansions.expand_with_filters(base_syntax_part5),
               syntax_expansions.definition_for_expansion_filters('nlp_number'),
               word_config.cfg_helpers['word_extent'], word_config.cfg_helpers['word_wkt_order'],
               word_config.cfg_helpers['team'])