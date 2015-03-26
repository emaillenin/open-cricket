from subprocess import call
import os
import gc
import glob
import codecs
from itertools import product
from collections import Counter
from os.path import basename
from opencricket.chart.sentence_parser import SentenceParser
import elasticsearch
from elasticsearch import helpers
from opencricket.config import es_config

EXPANSIONS = 'expansions'
SYNTAX = 'syntax'


class Productions:
    def __init__(self, es_host=None):
        self.es = es_config.es_builder(es_host)

    def productions(self):
        # TODO While producing expansions, do Map & Reduce instead of Iteration
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

        result.append({root: {SYNTAX: self.strip_permutation(self.dedup_syntax_list(root_productions),
                                                             parser.expandable_filters() + ['word_this_last']),
                              EXPANSIONS: syntax_expansions}})
        return result


    def explode(self, expansions_dir, exploded_dir):
        reference_expansions = {}
        for filename in glob.iglob(os.path.join(expansions_dir, '*.txt')):
            with codecs.open(filename, encoding='utf-8') as f:
                reference_expansions[os.path.splitext(basename(f.name))[0]] = f.read().splitlines()
        productions = self.productions()
        for production in productions:
            for key, syntax in production.items():
                exploded_filename = key + '.explosion'
                if os.path.exists(os.path.join(exploded_dir, exploded_filename)): os.remove(
                    os.path.join(exploded_dir, exploded_filename))
                syntax_list = syntax[SYNTAX]
                static_expansions = syntax[EXPANSIONS]
                for expansion_key, static_expansion in static_expansions.items():
                    reference_expansions[expansion_key] = static_expansion
                for s in syntax_list:
                    # TODO Throw error if any word without word_ is not present in reference
                    tmp = s
                    items_ = list(word for word in s.split())
                    for word in s.split():
                        tmp = tmp.replace(word, '%s')
                    final_items = list(reference_expansions[item] for item in items_)
                    with codecs.open(os.path.join(exploded_dir, exploded_filename), 'a', 'utf-8') as f:
                        f.write('\n'.join([tmp % a for a in list(product(*final_items))]) + '\n')


    def create_index(self):
        self.es.indices.create(index='opencricket', body=es_config.index_settings)
        self.es.indices.put_mapping(index='opencricket', doc_type='player_stats',
                                    body=es_config.type_mapping('player_stats'))

    def load_index(self, exploded_dir):
        for filename in glob.iglob(os.path.join(exploded_dir, '*')):
            call("cd %s && split -b 20000000 %s %s" % (
                exploded_dir, os.path.splitext(basename(filename))[0],
                os.path.splitext(basename(filename))[0] + '_oc_split'), shell=True)
            for split_file in glob.iglob(os.path.join(exploded_dir, '*_oc_split*')):
                print("Processing %s", split_file)
                with codecs.open(split_file, 'r', 'utf-8') as f:
                    actions = list({
                                       "_index": "opencricket",
                                       "_type": "player_stats",
                                       "_source": {
                                           "question": line.strip()
                                       }} for line in f)
                    elasticsearch.helpers.bulk(self.es, actions, chunk_size=200000)
                gc.collect()
            call("cd %s && rm *_oc_split*" % exploded_dir, shell=True)

    def delete_index(self):
        self.es.indices.delete(index='opencricket')

    def dedup_syntax_list(self, syntax_list):
        deduped_list = []
        for syntax in syntax_list:
            if not self.contains(deduped_list, syntax): deduped_list.append(syntax)
        return deduped_list

    def strip_permutation(self, syntax_list, possible_filters, upto=2):
        return list(syntax for syntax in syntax_list if len(set(syntax.split()).intersection(possible_filters)) <= upto)

    def contains(self, syntax_list, syntax):
        for s in syntax_list:
            if Counter(s.split()) == Counter(syntax.split()): return True
        return False
