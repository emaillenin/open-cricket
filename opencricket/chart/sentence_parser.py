import nltk
import logging
import os
import json
import re
import datetime
from opencricket.config import word_config
from opencricket.services.redis_service import RedisService
from opencricket.chart import syntax_expansions


class SentenceParser:
    def __init__(self, sentence, player_names=None):
        redis_service = RedisService()
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

        if not word_config.empty_pos(pos, 'NNP'):
            self.NNP = word_config.join_for_config(list(set(title_case_words + word_config.extract_words_with_tag(pos, 'NNP'))))
            self.player_names = word_config.join_for_config(
                list(set(title_case_words + word_config.extract_words_with_tag(pos, 'NNP') + player_names)))
        if not word_config.empty_pos(pos, 'CD'):
            self.CD = word_config.join_for_config(word_config.extract_words_with_tag(pos, 'CD'))

        word_config.cfg_helpers['nlp_player'] = """
            player -> player1 player2 player3
            player -> player1 player2
            player -> player1
            player1 -> %s
            player2 -> %s
            player3 -> %s
            """ % (self.player_names, self.player_names, self.player_names)
        word_config.cfg_helpers['nlp_ground'] = """
            ground -> ground1 ground2 ground3
            ground -> ground1 ground2
            ground -> ground1
            ground1 -> %s
            ground2 -> %s
            ground3 -> %s
            """ % (self.ground_names, self.ground_names, self.ground_names)

        word_config.cfg_helpers['nlp_number'] = self.CD

        self.cfg_parsers = []
        for key in redis_service.get_syntax_list():
            self.cfg_parsers.append(nltk.CFG.fromstring(
                syntax_expansions.replace_nlp_placeholders(redis_service.get_syntax(key))
            ))

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
