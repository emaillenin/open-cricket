import nltk
import logging
import os
import json
import re
from opencricket.config import word_config
from opencricket.chart import syntax_expansions


class SentenceParser:
    def __init__(self, sentence, player_names=None):

        if not player_names:
            player_names = []
        self.input = sentence.strip()
        title_case_pattern = re.compile('^[A-Z].*')
        title_case_words = list(
            set([word.lower() for word in self.input.split(' ') if title_case_pattern.match(word)] + [
                'default']) - word_config.ignore_title_case_words)

        self.input = sentence.lower().replace('?',
                                              '')  # Converting the input to lower case so we can specify only lower case words in config

        tokens = nltk.word_tokenize(self.input)
        pos = nltk.pos_tag(tokens)

        self.NNP = word_config.join_for_config(title_case_words)
        self.player_names = word_config.join_for_config(title_case_words + player_names)
        self.ground_names = word_config.join_for_config(list(set(title_case_words) - word_config.ignore_title_case_words))
        self.CD = '"0"'

        if not self.empty_pos(pos, 'NNP'):
            self.NNP = word_config.join_for_config(list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP'))))
            self.player_names = word_config.join_for_config(
                list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP') + player_names)))
        if not self.empty_pos(pos, 'CD'):
            self.CD = word_config.join_for_config(self.extract_words_with_tag(pos, 'CD'))

        word_config.cfg_helpers['player'] = """
            player -> player1 player2 player3
            player -> player1 player2
            player -> player1
            player1 -> %s
            player2 -> %s
            player3 -> %s
            """ % (self.player_names, self.player_names, self.player_names)
        word_config.cfg_helpers['ground'] = """
            ground -> ground1 ground2 ground3
            ground -> ground1 ground2
            ground -> ground1
            ground1 -> %s
            ground2 -> %s
            ground3 -> %s
            """ % (self.ground_names, self.ground_names, self.ground_names)

        word_config.cfg_helpers['nlp_number'] = self.CD

        self.cfg_parsers = []

        base_syntax_scores_team = "scores -> what_is_the word_extent word_score word_of team"
        base_syntax_scores_player = "scores -> what_is_the word_extent word_score word_of player"
        self.cfg_parsers.append(nltk.CFG.fromstring("""
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
                word_config.cfg_helpers['player'], word_config.cfg_helpers['team'],
                word_config.cfg_helpers['word_extent'],
                syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']))))

        base_syntax_part1 = 'partnerships -> word_extent word_partnership'
        base_syntax_part2 = 'partnerships -> word_extent word_partnership word_for word_wkt_order word_wicket'
        base_syntax_part3 = 'partnerships -> word_extent word_partnership word_for team'
        base_syntax_part4 = 'partnerships -> word_extent word_partnership word_for word_wkt_order word_wicket word_for team'
        base_syntax_part5 = 'partnerships -> word_extent word_partnership word_for team word_for word_wkt_order word_wicket'

        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
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
               syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
               word_config.cfg_helpers['word_extent'], word_config.cfg_helpers['word_wkt_order'],
               word_config.cfg_helpers['team'])))

        base_syntax_matches_cond_last_time = 'matches_cond -> last_time team word_chased target'
        base_syntax_matches_cond_how_many_times = 'matches_cond -> how_many_times team word_chased target'
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
                %s
                %s
                %s
                %s
                %s
                %s
                %s
                %s
                word_chased -> 'chased'
                target -> %s
            """ % (base_syntax_matches_cond_last_time, base_syntax_matches_cond_how_many_times,
                   syntax_expansions.expand_with_filters(base_syntax_matches_cond_how_many_times),
                   syntax_expansions.expand_with_filters(base_syntax_matches_cond_last_time),
                   syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
                   word_config.cfg_helpers['last_time'], word_config.cfg_helpers['how_many_times'], word_config.cfg_helpers['team'],
                   word_config.cfg_helpers['nlp_number']))
        )

        base_syntax_player_stats = """player_stats -> player word_stats"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            %s
            word_stats -> 'stats'
            """ % (
                base_syntax_player_stats,
                syntax_expansions.expand_with_filters(base_syntax_player_stats),
                syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
                word_config.cfg_helpers['player']))
        )

        base_syntax_most_x = """most_x -> who_player word_has word_the word_most metric"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            %s
            %s
            %s
            who_player -> word_who
            who_player -> word_which word_player
            who_player -> word_which teamplayer word_player
            word_who -> 'who'
            word_which -> 'which'
            word_player -> 'player'
            word_most -> 'highest' | 'most' | 'best'
            word_the -> 'the'
            """ % (base_syntax_most_x,
                   syntax_expansions.expand_with_filters(base_syntax_most_x),
                   syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
                   word_config.cfg_helpers['metric'],
                   word_config.cfg_helpers['word_has'], word_config.cfg_helpers['teamplayer']))
        )

        base_syntax_dismissals_with_team = 'player_dismissals -> word_dismissals word_by dismissals word_in team'
        base_syntax_dismissals = 'player_dismissals -> word_dismissals word_by dismissals'

        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
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
               syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
               word_config.cfg_helpers['team'],
               word_config.cfg_helpers['dismissals']))
        )

        base_syntax_compare = 'compare -> word_compare clause_player'
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
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
               syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
               word_config.cfg_helpers['player'],
               word_config.cfg_helpers['word_and']))
        )

        base_syntax_matches = """matches -> word_matches"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
                %s
                %s
                %s
                %s
                word_matches -> 'matches'
                team_A -> team
                team_B -> team
                %s
                %s
                """ % (base_syntax_matches, syntax_expansions.expand_with_filters(base_syntax_matches),
                       syntax_expansions.definition_for_expansion_filters(word_config.cfg_helpers['nlp_number']),
                       self.expand_with_matches_clauses(base_syntax_matches),
                       word_config.cfg_helpers['team'],
                       word_config.cfg_helpers['word_and'])))

    @staticmethod
    def str_wrap(string):
        return '"' + string + '"'

    @staticmethod
    def empty_pos(pos, tag):
        return len([p[0] for p in pos if p[1] == tag]) == 0

    @staticmethod
    def extract_words_with_tag(pos, tag):
        return [p[0] for p in pos if p[1] == tag]

    @staticmethod
    def words_from_pos(pos, tag):
        return '"' + '" | "'.join([p[0] for p in pos if p[1] == tag]) + '"'

    def expand_with_matches_clauses(self, base_syntax):
        final_syntax = ''
        for f in syntax_expansions.permutate_filters(word_config.expandable_match_clauses + word_config.expandable_filters_in):
            final_syntax += """
                                %s %s
                            """ % (base_syntax, ' '.join(f))
        final_syntax += """
                              %s
                              %s
                              %s
                              %s
                              %s
                              %s
                              wickets -> %s
                        """ % (
            syntax_expansions.build_syntax_with_expandable_filters('clause_result_by_team', word_config.match_clauses['clause_result_by_team']),
            syntax_expansions.build_syntax_with_expandable_filters('clause_between', word_config.match_clauses['clause_between']),
            # word_config.match_clauses['clause_batting_order'],
            # word_config.match_clauses['clause_innings_score'], word_config.match_clauses['clause_chasing_score'],
            # word_config.match_clauses['clause_wickets_left'],
            word_config.cfg_helpers['word_won'],
            word_config.cfg_helpers['word_between'],
            word_config.cfg_helpers['word_lost'],
            word_config.cfg_helpers['word_by'],
            word_config.cfg_helpers['nlp_number'])

        return final_syntax

    def parse_sentence(self):
        logging.basicConfig(
            filename=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/application.log',
            format='%(levelname)s %(asctime)s %(message)s',
            level=logging.INFO)
        logging.info("Input search: %s", self.input)
        for cfg in self.cfg_parsers:
            result = self.parse_input(cfg)
            if result is not None:
                return result

        logging.error("Unable to find result for : %s", self.input)
        return None

    def parse_input(self, grammar):
        try:
            result = nltk.ChartParser(grammar).parse(self.input.split())
            return self.send_result(result)
        except ValueError:
            pass

    def tree_to_dict(self, tree):
        tdict = {}
        for t in tree:
            if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
                tdict[t.label()] = self.tree_to_dict(t)
            elif isinstance(t, nltk.Tree):
                tdict[t.label()] = t[0]
        return tdict

    def dict_to_json(self, dictionary):
        return json.dumps(dictionary)

    def send_result(self, result):
        result_list = list(result)
        if len(result_list) > 0:
            json = self.dict_to_json({result_list[0].label(): self.tree_to_dict(result_list[0])})
            # result[0].draw()
            logging.info("Search Result " + json)
            return json
