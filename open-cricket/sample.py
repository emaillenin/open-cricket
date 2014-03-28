__author__ = 'Lenin Raj Rajasekaran'

import nltk, re, pprint


def extract(input):
    """

    :rtype : list of tuples for each work in the input string
    """
    return [nltk.pos_tag(sent) for sent in [nltk.word_tokenize(input)]]


grammar = "NP: {<DT>?<JJ>*<NN>}"
for line in open('./config/sentences.txt', 'r'):
    pos = extract(line)
    print(pos[0])
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pos[0])
    print result