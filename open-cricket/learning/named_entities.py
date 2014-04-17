__author__ = 'lrajasekaran'

import json
import sys
import nltk

# input = "What are the matches played between India and Australia in world cup?"
# input = 'What is Suresh Raina\'s scores this year?'
input = sys.stdin.readlines().__str__()
tokens = nltk.word_tokenize(input)
pos = nltk.pos_tag(tokens)
chunks = nltk.ne_chunk(pos)

result = {}
intent = 'match_list'
countries = []
players = []
series = []
matches = []

# print(chunks)
for a in chunks:
    if a.__class__.__name__ == 'Tree':
        if a.node == 'GPE':  # Detected a GPE. Can be either a country or a city (Ground)
            for b in a:
                countries.append(b[0])
        elif a.node == 'PERSON':  # Detected a Player name.
            players.append(' '.join(name for (name, pos) in a))

result['intent'] = intent
result['countries'] = countries
result['players'] = players
print(json.dumps(result))