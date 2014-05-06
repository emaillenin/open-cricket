from string import lower
import nltk
import sys
import logging
import os
import json

logging.basicConfig(filename=os.path.dirname(os.path.abspath(__file__)) + '/logs/application.log',
                    format='%(levelname)s %(asctime)s %(message)s',
                    level=logging.INFO)


def parse_input(grammar):
    try:
        result = nltk.ChartParser(grammar).nbest_parse(input.split())
        send_result(result)
    except ValueError:
        pass


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
    # input = 'matches between india and pakistan'
    input = 'highest scores of royal challengers bangalore'
    # input = 'matches between India and Pakistan'  # 2
    # input = 'highest partnerships for 1st wicket for south africa'

logging.info("Input search: %s", input)

tokens = nltk.word_tokenize(input)
pos = nltk.pos_tag(tokens)

NNP = '"' + '" | "'.join([p[0] for p in pos if p[1] == 'NNP']) + '"'

input = lower(input)  # Converting the input to lower case so we can specify only lower case words in config

team_list = "'india' | 'pakistan' | 'australia' | 'england' | 'zimbabwe' | 'bangladesh' | 'afghanistan' | 'kenya' | 'ireland' | 'netherlands' | 'netherland' | 'scotland' | 'canada' | 'bermuda' | 'namibia' | 'usa' | 'chennai' | 'super' | 'kings' | 'csk' | 'royal' |  'challengers' | 'bangalore' | 'rcb' | 'rajastan' | 'royals' | 'rr' | 'sunrisers' | 'hyderabad' | 'srh' | 'mumbai' | 'indians' | 'mi' | 'kings' | 'xi' | 'punjab' | 'kxip' | 'kolkata' | 'knight' | 'riders' | 'kkr' | 'pune' | 'warriors' | 'pwi' | 'delhi' | 'daredevils' | 'dd' | 'new' | 'zealand' | 'nz' | 'south' | 'africa' | 'sa' | 'sri' | 'lanka' | 'sl' | 'west' | 'indies' | 'wi' | 'uae' | 'east' | 'hong' | 'kong'"

cfg_helpers = {
    'extent': "extent -> 'highest' | 'lowest' | 'high' | 'low'",
    'wkt_order': "wkt_order -> '1st'| '2nd'| '3rd'| '4th'| '5th'| '6th'| '7th'| '8th'| '9th'| '10th'",
    'filler': "filler -> 'is' | 'are' | 'the' | 'scores' | 'score' | 'for' | 'by' | 'of'",
    'team': """
            team -> team1 team2 team3
            team -> team1 team2
            team -> team1
            team1 -> """ + team_list + """
            team2 -> """ + team_list + """
            team3 -> """ + team_list + """
            """,
}
cfg_parsers = []

cfg_parsers.append(
    nltk.parse_cfg("""
 matches -> select clause
 matches -> select IN clause
 clause -> teamA CC teamB
 select -> 'matches' | 'match' | 'games' | 'game'
 teamA -> team
 teamB -> team
 %s
 CC -> 'and' | '&' | 'vs'
 IN -> 'between' | 'of'
 """ % cfg_helpers['team']))
cfg_parsers.append(nltk.parse_cfg("""
 scores -> question filler extent filler team
 scores -> extent filler team
 scores -> extent class filler team
 %s
 question -> 'what'
 %s
 class -> 'ODI' | 'test'
 filler -> filler filler
 filler -> 'is' | 'are' | 'the' | 'scores' | 'score' | 'for' | 'by' | 'of'
 IN -> 'between' | 'of'
 """ % (cfg_helpers['team'], cfg_helpers['extent'])))

cfg_parsers.append(
    nltk.parse_cfg("""
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
""" % (cfg_helpers['extent'], cfg_helpers['filler'], cfg_helpers['wkt_order'], cfg_helpers['team'])))

# @doc - Recursive grammer (filler -> filler filler) will not be captured in dictionary since they have the same key. This is okay since we dont use this info for Search

for cfg in cfg_parsers:
    parse_input(cfg)

logging.error("Unable to find result for : %s", input)
exit(2)