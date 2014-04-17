import nltk


def str_wrap(str):
    return '"' + str + '"'


def tree_to_list(tree):  # convert tree to list
    result = ''
    if isinstance(tree, nltk.Tree) and isinstance(tree[0], nltk.Tree):
        result += str_wrap(tree.node) + ' : ' + "{\n" + ",\n".join([tree_to_list(t) for t in tree]) + "\n}"
    elif isinstance(tree, nltk.Tree):
        result += str_wrap(tree.node) + ' : ' + str_wrap(tree[0])
    else:
        result += str_wrap(tree) + ",\n"
    return result


def analyze_tree(tree):
    for t in tree:
        print(t.node)
        print(len(t))
        print(t[0].__class__)
        if t[0].__class__.__name__ == 'Tree': analyze_tree(t[0])


input = 'highest scores for India'
# input = 'India'
tokens = nltk.word_tokenize(input)
pos = nltk.pos_tag(tokens)

NNP = '"' + '" | "'.join([p[0] for p in pos if p[1] == 'NNP']) + '"'

if False:
    grammar = nltk.parse_cfg("""
     S -> team
     team -> %s
     """ % NNP)

grammar = nltk.parse_cfg("""
 S -> select clause
 S -> select IN clause
 clause -> team CC team
 select -> 'matches' | 'match' | 'games' | 'game'
 team -> %s
 CC -> 'and' | '&' | 'vs'
 IN -> 'between' | 'of'
 """ % NNP)

result = nltk.ChartParser(grammar).nbest_parse(input.split())
# result[0].draw()

print("{\n" + tree_to_list(result[0]) + "\n}")
