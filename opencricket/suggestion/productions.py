import json
import os
import glob
import codecs
from itertools import product
from collections import Counter
from os.path import basename
from opencricket.chart.sentence_parser import SentenceParser
from _datetime import datetime
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from opencricket.config import es_config
EXPANSIONS = 'expansions'
SYNTAX = 'syntax'


class Productions:

    def __init__(self, es_host = None):
        if(es_host == None): es_host = '127.0.0.1'
        self.es = Elasticsearch(hosts=es_host)

    def productions(self):
        # TODO While producing expansions, use Map Reduce instead of Iteration
        result = []
        parser = SentenceParser('')
        stats_parser = parser.cfg_parsers[4]
        player_stats_productions = stats_parser.productions()
        root = player_stats_productions[0].lhs()._symbol
        root_productions = []
        syntax_expansions = {}
        for p in player_stats_productions:
            syntax = p.__str__()
            syntax_split = syntax.split(' -> ')
            if syntax_split[0] == root: root_productions.append(syntax_split[1])
            for key in stats_parser._leftcorner_words.keys():
                if key.__str__().startswith('word_'):
                    syntax_expansions[key.__str__()] = list(stats_parser._leftcorner_words[key])

        result.append({root: {SYNTAX: root_productions, EXPANSIONS: syntax_expansions}})
        return json.dumps(result)


    def explode(self, expansions_dir, exploded_dir):
        reference_expansions = {}
        for filename in glob.iglob(os.path.join(expansions_dir, '*.txt')):
            with codecs.open(filename, encoding='utf-8') as f:
                reference_expansions[os.path.splitext(basename(f.name))[0]] = f.read().splitlines()
        productions = json.loads(self.productions())
        for production in productions:
            for key, syntax in production.items():
                if (os.path.exists(os.path.join(exploded_dir, key))): os.remove(os.path.join(exploded_dir, key))
                print(len(syntax[SYNTAX]))
                syntax_list = self.dedup_syntax_list(syntax[SYNTAX])
                print(len(syntax_list))
                static_expansions = syntax[EXPANSIONS]
                for expansion_key, static_expansion in static_expansions.items():
                    reference_expansions[expansion_key] = static_expansion
                for s in syntax_list:
                    # TODO Throw error if any word without word_ is not present in reference
                    tmp = s
                    items_ = [word for word in s.split()]
                    for word in s.split():
                        tmp = tmp.replace(word, '%s')
                    final_items = [reference_expansions[item] for item in items_]
                    with codecs.open(os.path.join(exploded_dir, key), 'a', 'utf-8') as f:
                        f.write('\n'.join([tmp % a for a in list(product(*final_items))]) + '\n')


    def create_index(self):
        self.es.indices.create(index='opencricket', body=es_config.index_settings)
        self.es.indices.put_mapping(index='opencricket', doc_type='player_stats', body=es_config.mapping)

    def load_index(self, exploded_dir):
        with codecs.open(os.path.join(exploded_dir, 'player_stats'), 'r', 'utf-8') as f:
            actions = [{
                           "_index": "opencricket",
                           "_type": "player_stats",
                           "_source": {
                               "question": line
                           }} for line in f]
            elasticsearch.helpers.bulk(self.es,actions, chunk_size=100000)
        return json.dumps({'status': 'ok'})

    def delete_index(self):
        self.es.indices.delete(index='opencricket')

    def dedup_syntax_list(self, syntax_list):
        deduped_list = []
        for syntax in syntax_list:
            if not self.contains(deduped_list, syntax): deduped_list.append(syntax)
        print(deduped_list)
        return deduped_list

    def contains(self, syntax_list, syntax):
        for s in syntax_list:
            if Counter(s.split()) == Counter(syntax.split()): return True
        return False