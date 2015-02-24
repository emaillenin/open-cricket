import nltk
import logging
import os
import json
import re
import itertools


class SentenceParser:
    def __init__(self, sentence, player_names=None):

        if not player_names:
            player_names = []
        self.input = sentence
        title_case_pattern = re.compile('^[A-Z].*')
        title_case_words = [word.lower() for word in self.input.split(' ') if title_case_pattern.match(word)] + [
            'default']

        self.input = sentence.lower().replace('?',
                                              '')  # Converting the input to lower case so we can specify only lower case words in config

        tokens = nltk.word_tokenize(self.input)
        pos = nltk.pos_tag(tokens)

        self.NNP = self.join_for_config(title_case_words)
        self.player_names = self.join_for_config(title_case_words + player_names)
        self.CD = '"0"'

        if not self.empty_pos(pos, 'NNP'):
            self.NNP = self.join_for_config(list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP'))))
            self.player_names = self.join_for_config(
                list(set(title_case_words + self.extract_words_with_tag(pos, 'NNP') + player_names)))
        if not self.empty_pos(pos, 'CD'):
            self.CD = self.join_for_config(self.extract_words_with_tag(pos, 'CD'))

        filler_list = self.join_for_config(
            ['is', 'are', 'the', 'scores', 'score', 'for', 'by', 'of', 'in', 'has', 'at'])
        team_list = self.join_for_config(
            ['india', 'pakistan', 'australia', 'england', 'zimbabwe', 'bangladesh', 'afghanistan', 'kenya', 'ireland',
             'netherlands', 'netherland', 'scotland', 'canada', 'bermuda', 'namibia', 'usa', 'chennai', 'super',
             'kings', 'csk', 'royal', 'challengers', 'bangalore', 'rcb', 'rajastan', 'royals', 'rr', 'sunrisers',
             'hyderabad', 'srh', 'mumbai', 'indians', 'mi', 'kings', 'xi', 'punjab', 'kxip', 'kolkata', 'knight',
             'riders', 'kkr', 'pune', 'warriors', 'pwi', 'delhi', 'daredevils', 'dd', 'new', 'zealand', 'nz', 'south',
             'africa', 'sa', 'sri', 'lanka', 'sl', 'west', 'indies', 'wi', 'uae', 'east', 'hong', 'kong'])
        series_list = self.join_for_config(
            ['ipl', 'indian', 'premier', 'league', 'champions', 'league', 't20', 'world', 'cup', 'clt20',
             't20', 'trophy', 'icc', 'twenty20'])
        metric_list = self.join_for_config(
            ['fifties', 'sixes', 'fours', '100s', 'hundreds', 'centuries', 'matches', 'innings', 'runs',
             'wickets'])
        match_type_list = ['test', 'odi', 't20i', 't20']

        self.cfg_helpers = {
            'word_in': "word_in -> 'in'",
            'word_has': "word_has -> 'has'",
            'word_articles': "word_articles -> 'a' | 'an' | 'the'",
            'word_this_last': "word_this_last -> 'this' | 'last'",
            'extent': "extent -> 'highest' | 'lowest' | 'high' | 'low'",
            'cc': "CC -> 'and' | '&' | 'vs'",
            'wkt_order': "wkt_order -> '1st'| '2nd'| '3rd'| '4th'| '5th'| '6th'| '7th'| '8th'| '9th'| '10th'",
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
                    """ % (self.NNP, self.NNP, self.NNP),
            'series': """
                    series -> series1 series2 series3
                    series -> series1 series2
                    series -> series1
                    series1 -> """ + series_list + """
                    series2 -> """ + series_list + """
                    series3 -> """ + series_list + """
                    """,
            'metric': """
                    metric -> %s
                    """ % metric_list,
            'in_match_type': """
                    match_type -> %s
                    """ % self.join_for_config(match_type_list),
            'last_time': """
                    last_time -> when was the last time
                    when -> 'when'
                    was -> 'was'
                    the -> 'the'
                    last -> 'last'
                    time -> 'time'
                    """,
            'how_many_times': """
                    how_many_times -> how many times
                    how -> 'how'
                    many -> 'many'
                    times -> 'times'
                    """
        }

        self.cfg_parsers = []

        base_syntax_matches = """matches -> select IN clause"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
                %s
                %s
                clause -> teamA CC teamB
                select -> 'matches' | 'match' | 'games' | 'game'
                teamA -> team
                teamB -> team
                %s
                %s
                IN -> 'between' | 'of'
                """ % (base_syntax_matches, self.expand_with_filters(base_syntax_matches), self.cfg_helpers['team'],
                       self.cfg_helpers['cc'])))

        self.cfg_parsers.append(nltk.CFG.fromstring("""
             scores -> question filler extent filler team
             scores -> extent filler team
             scores -> extent class filler team
             scores -> player period filler
             period -> 'recent' | 'best' | 'highest'
             %s
             %s
             question -> 'what'
             %s
             class -> 'ODI' | 'test'
             filler -> filler1 filler2
             filler1 -> filler
             filler2 -> filler
             %s
             IN -> 'between' | 'of'
         """ % (
            self.cfg_helpers['player'], self.cfg_helpers['team'], self.cfg_helpers['extent'],
            self.cfg_helpers['filler'])))

        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            partnerships -> extent select
            partnerships -> select extent
            partnerships -> extent select filler wkt_order wicket
            partnerships -> extent select filler wkt_order wicket filler team
            partnerships -> extent select filler team
            partnerships -> extent select filler team filler wkt_order wicket
            select -> 'partnership' |  'partnerships'
            %s
            %s
            %s
            %s
            wicket -> 'wicket'
        """ % (self.cfg_helpers['extent'], self.cfg_helpers['filler'], self.cfg_helpers['wkt_order'],
               self.cfg_helpers['team'])))

        base_syntax_matches_cond = 'matches_cond -> what team chased_s score'
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
                %s
                %s
                what -> last_time
                what -> how_many_times
                %s
                %s
                %s
                chased_s -> chased
                chased_s -> chased down
                chased -> 'chased' | 'chase'
                down -> 'down'
                score -> %s
            """ % (base_syntax_matches_cond, self.expand_with_filters(base_syntax_matches_cond),
                   self.cfg_helpers['last_time'], self.cfg_helpers['how_many_times'], self.cfg_helpers['team'],
                   self.CD))
        )

        base_syntax_player_stats = """player_stats -> player word_stats"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            word_stats -> 'stats' | 'statistics' | 'scores' | 'runs' | 'wickets' | 'career'
            """ % (
                base_syntax_player_stats, self.expand_with_filters(base_syntax_player_stats),
                self.cfg_helpers['player']))
        )

        base_syntax_most_x = """most_x -> who_player word_has word_articles most metric"""
        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            %s
            %s
            %s
            %s
            %s
            who_player -> who
            who_player -> which_player
            who -> 'who'
            which_player -> which player
            which -> 'which'
            player -> 'player'
            most -> 'most'
            """ % (base_syntax_most_x, self.expand_with_filters(base_syntax_most_x), self.cfg_helpers['metric'], self.cfg_helpers['word_articles'], self.cfg_helpers['word_has']))
        )

        self.cfg_parsers.append(
            nltk.CFG.fromstring("""
            player_dismissals -> what filler dismissals filler team
            player_dismissals -> what filler dismissals
            what -> 'dismissals'
            %s
            %s
            %s
        """ % (self.cfg_helpers['filler'], self.cfg_helpers['team'], self.cfg_helpers['dismissals']))
        )

        base_syntax_compare = 'compare -> compare_word player_1 CC player_2'
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
               self.cfg_helpers['cc']))
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
                              year -> %s
                              year -> 'year'
                        """ % (self.cfg_helpers['series'], self.cfg_helpers['word_this_last'],self.cfg_helpers['word_in'],
                               self.cfg_helpers['in_match_type'], self.cfg_helpers['ground'], self.CD)
        return final_syntax

    @staticmethod
    def permutate_filters():
        filters = ['match_type', 'series', 'year', 'ground']
        permutated_filters = []
        for i in range(1, len(filters) + 1):
            for f in itertools.permutations(filters, i):
                permutated_filters += [list(f)]
                if 'year' in f:
                    this_last_year_list = list(f)
                    this_last_year_list[this_last_year_list.index('year')] = 'word_this_last year'
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
