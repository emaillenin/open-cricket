import nltk
import logging
import os
import json
import re
import itertools
from opencricket.config import word_config

from nltk.parse import generate
from nltk.grammar import Nonterminal


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

        self.NNP = self.join_for_config(title_case_words)
        self.player_names = self.join_for_config(title_case_words + player_names)
        self.ground_names = self.join_for_config(list(set(title_case_words) - word_config.ignore_title_case_words))
        self.CD = '"0"'

        if not self.empty_pos(pos, 'NNP'):
            self.NNP = self.join_for_config(list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP'))))
            self.player_names = self.join_for_config(
                list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP') + player_names)))
        if not self.empty_pos(pos, 'CD'):
            self.CD = self.join_for_config(self.extract_words_with_tag(pos, 'CD'))

        filler_list = self.join_for_config(
            ['is', 'are', 'the', 'scores', 'score', 'for', 'by', 'of', 'in', 'has', 'at'])

        team_list = self.join_for_config(self.split_and_form_list(self.team_names_list()))
        team_player_list = self.join_for_config(self.split_and_form_list(self.team_player_list()))

        series_list = self.join_for_config(
            ['ipl', 'indian', 'premier', 'league', 'champions', 'league', 'world', 'cup', 'clt20',
             't20', 'trophy', 'icc', 'twenty20'])
        metric_list = self.join_for_config(
            ['fifties', 'sixes', 'fours', '100s', '50s', '30s', 'hundreds', 'centuries', 'matches', 'innings', 'runs',
             'wickets', 'not', 'outs', 'high', 'individual', 'score', 'balls', 'faced', 'minutes', 'strike', 'rate',
             'average', 'thirties', 'bowled', 'maiden', 'over', 'overs', 'conceded', 'best', 'bowling', 'figure',
             'catches', 'stumpings', 'economy', 'five', 'wicket', 'haul', 'ten'])
        match_type_list = ['test', 'odi', 't20i', 't20']

        # TODO A dynamic generator for 'word' helpers
        self.cfg_helpers = {
            'word_in': "word_in -> 'in'",
            'word_has': "word_has -> 'has'",
            'word_articles': "word_articles -> 'a' | 'an' | 'the'",
            'word_this_last': "word_this_last -> 'this' | 'last'",
            'word_year': "word_year -> 'year'",

            'word_extent': "word_extent -> 'highest' | 'lowest' | 'recent'",
            'word_and': "word_and -> 'and'",
            'word_wkt_order': "word_wkt_order -> '1st'| '2nd'| '3rd'| '4th'| '5th'| '6th'| '7th'| '8th'| '9th'| '10th'",
            'filler': """
                    filler -> %s
                    """ % filler_list,
            'dismissals': "dismissals -> 'bowled' | 'caught' | 'lbw' | 'run out' | 'stumping' | 'hit_wicket'",
            'team': """
                    team -> team1 team2 team3
                    team -> team1 team2
                    team -> team1
                    team1 -> """ + team_list + """
                    team2 -> """ + team_list + """
                    team3 -> """ + team_list + """
                    """,
            'team_player': """
                    team_player -> team_player1 team_player2 team_player3
                    team_player -> team_player1 team_player2
                    team_player -> team_player1
                    team_player1 -> """ + team_player_list + """
                    team_player2 -> """ + team_player_list + """
                    team_player3 -> """ + team_player_list + """
                    """,
            'player': """
                    player -> player1 player2 player3
                    player -> player1 player2
                    player -> player1
                    player1 -> %s
                    player2 -> %s
                    player3 -> %s
                    """ % (self.player_names, self.player_names, self.player_names),
            'ground': """
                    ground -> ground1 ground2 ground3
                    ground -> ground1 ground2
                    ground -> ground1
                    ground1 -> %s
                    ground2 -> %s
                    ground3 -> %s
                    """ % (self.ground_names, self.ground_names, self.ground_names),
            'series': """
                    series -> series1 series2 series3
                    series -> series1 series2
                    series -> series1
                    series1 -> """ + series_list + """
                    series2 -> """ + series_list + """
                    series3 -> """ + series_list + """
                    """,
            'metric': """
                    metric -> metric1 metric2 metric3
                    metric -> metric1 metric2
                    metric -> metric1
                    metric1 -> """ + metric_list + """
                    metric2 -> """ + metric_list + """
                    metric3 -> """ + metric_list + """
                    """,
            'in_match_type': """
                    match_type -> %s
                    """ % self.join_for_config(match_type_list),
            'last_time': """
                    last_time -> word_when word_was word_the word_last word_time
                    word_when -> 'when'
                    word_was -> 'was'
                    word_the -> 'the'
                    word_last -> 'last'
                    word_time -> 'time'
                    """,
            'how_many_times': """
                    how_many_times -> word_how word_many word_times
                    word_how -> 'how'
                    word_many -> 'many'
                    word_times -> 'times'
                    """
        }

        self.cfg_parsers = []

        base_syntax_matches = """matches -> word_select word_between clause"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
                %s
                %s
                clause -> team_A word_and team_B
                word_select -> 'matches'
                team_A -> team
                team_B -> team
                %s
                %s
                word_between -> 'between'
                """ % (base_syntax_matches, self.expand_with_filters(base_syntax_matches), self.cfg_helpers['team'],
                       self.cfg_helpers['word_and'])))

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
         """ % (base_syntax_scores_team, base_syntax_scores_player, self.expand_with_filters(base_syntax_scores_team),
                self.expand_with_filters(base_syntax_scores_player),
                self.cfg_helpers['player'], self.cfg_helpers['team'], self.cfg_helpers['word_extent'])))

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
            word_for -> 'for'
            word_wicket -> 'wicket'
        """ % (base_syntax_part1, base_syntax_part2, base_syntax_part3, base_syntax_part4, base_syntax_part5,
               self.expand_with_filters(base_syntax_part1), self.expand_with_filters(base_syntax_part2),
               self.expand_with_filters(base_syntax_part3), self.expand_with_filters(base_syntax_part4),
               self.expand_with_filters(base_syntax_part5),
               self.cfg_helpers['word_extent'], self.cfg_helpers['word_wkt_order'],
               self.cfg_helpers['team'])))

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
                word_chased -> 'chased'
                target -> %s
            """ % (base_syntax_matches_cond_last_time, base_syntax_matches_cond_how_many_times,
                   self.expand_with_filters(base_syntax_matches_cond_how_many_times),
                   self.expand_with_filters(base_syntax_matches_cond_last_time),
                   self.cfg_helpers['last_time'], self.cfg_helpers['how_many_times'], self.cfg_helpers['team'],
                   self.CD))
        )

        base_syntax_player_stats = """player_stats -> player word_stats"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            word_stats -> 'stats'
            """ % (
                base_syntax_player_stats, self.expand_with_filters(base_syntax_player_stats),
                self.cfg_helpers['player']))
        )

        base_syntax_most_x = """most_x -> who_player word_has word_the word_most metric"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            %s
            %s
            who_player -> word_who
            who_player -> word_which word_player
            who_player -> word_which team_player word_player
            word_who -> 'who'
            word_which -> 'which'
            word_player -> 'player'
            word_most -> 'highest' | 'most' | 'best'
            word_the -> 'the'
            """ % (base_syntax_most_x, self.expand_with_filters(base_syntax_most_x), self.cfg_helpers['metric'],
                   self.cfg_helpers['word_has'], self.cfg_helpers['team_player']))
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
            word_in -> 'in'
            word_by -> 'by'
        """ % (base_syntax_dismissals_with_team, base_syntax_dismissals,
               self.expand_with_filters(base_syntax_dismissals_with_team),
               self.expand_with_filters(base_syntax_dismissals), self.cfg_helpers['team'],
               self.cfg_helpers['dismissals']))
        )

        base_syntax_compare = 'compare -> compare_word player_1 word_and player_2'
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            player_1 -> player
            player_2 -> player
            compare_word -> 'compare'
            %s
            %s
        """ % (base_syntax_compare, self.expand_with_filters(base_syntax_compare), self.cfg_helpers['player'],
               self.cfg_helpers['word_and']))
        )


    @staticmethod
    def join_for_config(words):
        return ' "' + '" | "'.join(words) + '" '

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

    @staticmethod
    def split_and_form_list(source):
        return list(set(sum([s.split() for s in source], [])))

    def expand_with_filters(self, base_syntax):
        final_syntax = ''
        for f in self.permutate_filters():
            final_syntax += """
                                %s word_in %s
                            """ % (base_syntax, ' word_in '.join(f))
        final_syntax += """
                              %s
                              %s
                              %s
                              %s
                              %s
                              %s
                              year -> %s
                        """ % (
            self.cfg_helpers['ground'], self.cfg_helpers['word_this_last'], self.cfg_helpers['word_in'],
            self.cfg_helpers['word_year'],
            self.cfg_helpers['series'], self.cfg_helpers['in_match_type'], self.CD)
        return final_syntax

    @staticmethod
    def expandable_filters():
        return ['match_type', 'series', 'year', 'ground']

    @staticmethod
    def team_names_list():
        return ['india', 'pakistan', 'australia', 'england', 'zimbabwe', 'bangladesh', 'afghanistan', 'kenya',
                'ireland', 'netherlands', 'scotland', 'canada', 'bermuda', 'namibia', 'usa', 'chennai super kings',
                'csk', 'royal challengers bangalore', 'rcb', 'rajastan royals', 'rr', 'sunrisers hyderabad', 'srh',
                'mumbai indians', 'mi', 'kings xi punjab', 'kxip', 'kolkata knight riders', 'kkr', 'pune warriors',
                'pwi', 'delhi daredevils', 'dd', 'new zealand', 'nz', 'south africa', 'sa', 'sri lanka', 'sl',
                'west indies',
                'wi', 'uae', 'east africa', 'hong kong']

    @staticmethod
    def team_player_list():
        return SentenceParser.team_names_list() + ['indian', 'australian', 'kenyan', 'canadian', 'namibian', 'african',
                                                   'lankan', 'pakistani']

    def permutate_filters(self):
        filters = self.expandable_filters()
        permutated_filters = []
        for i in range(1, len(filters) + 1):
            for f in itertools.permutations(filters, i):
                permutated_filters += [list(f)]
                if 'year' in f:
                    this_last_year_list = list(f)
                    this_last_year_list[this_last_year_list.index('year')] = 'word_this_last word_year'
                    permutated_filters += [this_last_year_list]
        return permutated_filters

    def parse_sentence(self):
        logging.basicConfig(
            filename=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/logs/application.log',
            format='%(levelname)s %(asctime)s %(message)s',
            level=logging.INFO)
        logging.info("Input search: %s", self.input)
        for cfg in self.cfg_parsers:
            result = self.parse_input(cfg)
            if result is not None: return result

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
