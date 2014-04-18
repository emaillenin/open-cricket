import nltk
import sys
import logging
import os
import json

logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + '/logs/application.log',
                    format='%(levelname)s %(asctime)s %(message)s',
                    level=logging.INFO)


def parse_input(grammar):
    result = []
    try:
        result = nltk.ChartParser(grammar).nbest_parse(input.split())
    except ValueError:
        pass
    send_result(result)


def str_wrap(str):
    return '"' + str + '"'


def tree_to_list(tree):  # convert tree to list
    result = ''
    if isinstance(tree, nltk.Tree) and isinstance(tree[0], nltk.Tree):
        result += str_wrap(tree.node) + ' : ' + ",".join([tree_to_list(t) for t in tree]) + "  }"
    elif isinstance(tree, nltk.Tree):
        result += str_wrap(tree.node) + ' : ' + str_wrap(tree[0])
    else:
        result += str_wrap(tree) + ",  "
    return result


def tree_to_dict(tree):
    tdict = {}
    for t in tree:
        if isinstance(t, nltk.Tree) and isinstance(t[0], nltk.Tree):
            tdict[t.node] = tree_to_dict(t)
        elif isinstance(t, nltk.Tree):
            tdict[t.node] = t[0]
    return tdict


def dict_to_json(dict):
    return json.dumps(dict)


def analyze_tree(tree):
    for t in tree:
        print(t.node)
        print(len(t))
        print(t[0].__class__)
        if t[0].__class__.__name__ == 'Tree': analyze_tree(t[0])


def send_result(result):
    if len(result) > 0:
        # json = tree_to_list(result[0])
        json = dict_to_json({result[0].node: tree_to_dict(result[0])})
        # result[0].draw()
        logging.info("Search Result " + json)
        print(json)
        exit(0)


if len(sys.argv) > 1:
    input = ' '.join(sys.argv[1:])
else:
    #  TODO Please do Unit test for each type of input. Unit test should check the final json output.
    # input = 'matches India and Pakistan'
    input = 'highest scores for India'  # 2

logging.info("Input search: %s", input)

tokens = nltk.word_tokenize(input)
pos = nltk.pos_tag(tokens)

NNP = '"' + '" | "'.join([p[0] for p in pos if p[1] == 'NNP']) + '"'

if False:
    grammar = nltk.parse_cfg("""
     S -> team
     team -> %s
     """ % NNP)

matches = nltk.parse_cfg("""
 matches -> select clause
 matches -> select IN clause
 clause -> team1 CC team2
 select -> 'matches' | 'match' | 'games' | 'game'
 team1 -> team
 team2 -> team
 team -> %s
 CC -> 'and' | '&' | 'vs'
 IN -> 'between' | 'of'
 """ % NNP)

scores = nltk.parse_cfg("""
 scores -> question filler extent filler team
 scores -> extent filler team
 scores -> extent class filler team
 team -> %s
 question -> 'what'
 extent -> 'highest' | 'lowest' | 'high' | 'low'
 class -> 'ODI' | 'test'
 filler -> filler filler
 filler -> 'is' | 'are' | 'the' | 'scores' | 'score' | 'for' | 'by' | 'of'
 IN -> 'between' | 'of'
 """ % NNP)

# @doc - Recursive grammer (filler -> filler filler) will not be captured in dictionary since they have the same key. This is okay since we dont use this info for Search

parse_input(matches)

parse_input(scores)

logging.error("Unable to find result for : %s", input)
exit(2)