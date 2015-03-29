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
from nltk.grammar import Nonterminal

EXPANSIONS = 'expansions'
DYNAMIC_EXPANSIONS = 'dynamic_expansions'
SYNTAX = 'syntax'


class Productions:
    def __init__(self, es_host=None):
        self.es = es_config.es_builder(es_host)

    def productions(self, expansions_dir):
        # TODO While producing expansions, do Map & Reduce instead of Iteration
        result = []
        parser = SentenceParser('')
        expansion_files = list(
            os.path.splitext(basename(f))[0] for f in glob.iglob(os.path.join(expansions_dir, '*.txt')))
        # for stats_parser in parser.cfg_parsers:
        stats_parser = parser.cfg_parsers[2]
        root = str(stats_parser.start())
        root_productions = stats_parser.productions(lhs=Nonterminal(root))
        result_productions = []
        syntax_expansions = {}
        dynamic_expansions = {}
        for p in root_productions:
            syntax = str(p)
            syntax_split = syntax.split(' -> ')
            result_productions.append(syntax_split[1])
        for key in stats_parser._leftcorner_words.keys():
            if str(key).startswith('word_'):
                syntax_expansions[str(key)] = list(stats_parser._leftcorner_words[key])
        for s in stats_parser._lhs_index:
            key = str(s).split(' -> ')[0]
            if key == root or any(char.isdigit() for char in key) or key.startswith('word_') or any(
                    key.startswith(f) for f in expansion_files):
                continue
            for p in stats_parser.productions(lhs=s):
                dynamic_expansions[str(s).split(' -> ')[0]] = ' '.join(map(str, p.rhs()))
        result.append({root: {SYNTAX: self.strip_permutation(self.dedup_syntax_list(result_productions),
                                                             parser.expandable_filters() + ['word_this_last']),
                              EXPANSIONS: syntax_expansions,
                              DYNAMIC_EXPANSIONS: dynamic_expansions
                              }})
        return result


    def explode(self, expansions_dir, exploded_dir):
        reference_expansions = {}
        for filename in glob.iglob(os.path.join(expansions_dir, '*.txt')):
            with codecs.open(filename, encoding='utf-8') as f:
                reference_expansions[os.path.splitext(basename(f.name))[0]] = f.read().splitlines()
        productions = self.productions(expansions_dir)
        for production in productions:
            for key, syntax in production.items():
                exploded_filename = key
                if os.path.exists(os.path.join(exploded_dir, exploded_filename)): os.remove(
                    os.path.join(exploded_dir, exploded_filename))
                syntax_list = syntax[SYNTAX]
                static_expansions = syntax[EXPANSIONS]
                dynamic_expansions = syntax[DYNAMIC_EXPANSIONS]
                for expansion_key, static_expansion in static_expansions.items():
                    reference_expansions[expansion_key] = static_expansion
                for expansion_key, dynamic_expansion in dynamic_expansions.items():
                    tmp = ' '.join(['%s'] * len(dynamic_expansion.split()))
                    final_items = list(
                        reference_expansions[item if item.startswith('word_') else item.split('_')[0]] for item in
                        dynamic_expansion.split())
                    reference_expansions[expansion_key] = list(tmp % a for a in list(product(*final_items)))
                for s in syntax_list:
                    # TODO Throw error if any word without word_ is not present in reference
                    tmp = ' '.join(['%s'] * len(s.split()))
                    final_items = list(reference_expansions[item] for item in s.split())
                    with codecs.open(os.path.join(exploded_dir, exploded_filename), 'a', 'utf-8') as f:
                        f.write('\n'.join([tmp % a for a in list(product(*final_items))]) + '\n')


    def create_index(self):
        self.es.indices.create(index='opencricket', body=es_config.index_settings)
        parser = SentenceParser('')
        for doc_type in list(map(str, (p.start() for p in parser.cfg_parsers))):
            self.put_mapping(doc_type)

    def put_mapping(self, doc_type):
        self.es.indices.put_mapping(index='opencricket', doc_type=doc_type,
                                        body=es_config.type_mapping(doc_type))

    def load_index(self, exploded_dir):
        for filename in glob.iglob(os.path.join(exploded_dir, '*')):
            doc_type = os.path.splitext(basename(filename))[0]
            self.put_mapping(doc_type)
            call("cd %s && rm *_oc_split*" % exploded_dir, shell=True)
            call("cd %s && split -b 20000000 %s %s" % (
                exploded_dir, doc_type,
                doc_type + '_oc_split'), shell=True)
            for split_file in glob.iglob(os.path.join(exploded_dir, '*_oc_split*')):
                print("Processing %s" % split_file)
                with codecs.open(split_file, 'r', 'utf-8') as f:
                    actions = list({
                                       "_index": "opencricket",
                                       "_type": doc_type,
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
