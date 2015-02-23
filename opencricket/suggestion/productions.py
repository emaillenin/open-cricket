import json
from opencricket.chart.sentence_parser import SentenceParser


class Productions:
    # def __init__(self):

    def productions(self):
        result = []
        parser = SentenceParser('')
        stats_parser = parser.cfg_parsers[4]
        player_stats_productions = stats_parser.productions()
        root = player_stats_productions[0].lhs()._symbol
        root_productions = []
        syntax_expansions = []
        for p in player_stats_productions:
            syntax = p.__str__()
            syntax_split = syntax.split(' -> ')
            if syntax_split[0] == root: root_productions.append(syntax_split[1])
        expansions = {key.__str__(): list(stats_parser._leftcorner_words[key]) for key in stats_parser._leftcorner_words.keys() if
         key.__str__().startswith('word_')}
        syntax_expansions.append(expansions)

        result.append({root: {'syntax': root_productions, 'expansions': syntax_expansions}})
        return json.dumps(result)