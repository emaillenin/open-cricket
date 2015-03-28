
import nltk
from nltk.parse import generate
from nltk.grammar import Nonterminal


cfg = nltk.CFG.fromstring("""
root -> who_player has the most runs
who_player -> who
who_player -> which player
who_player -> which team player
who -> 'who'
which -> 'which'
player -> 'player'
team -> 'indian' | 'australian' | 'england' | 'sri lankan'
has -> 'has'
the -> 'the'
this -> 'this'
most -> 'most'
runs -> 'runs'
""")

print(list((n,sent) for n, sent in enumerate(generate.generate(cfg, n=100, start=Nonterminal('root')), 1)))

result1 = nltk.ChartParser(cfg).parse('which england player has the most runs'.split())
result2 = nltk.ChartParser(cfg).parse(['which', 'sri lankan', 'player', 'has', 'the', 'most',  'runs'])
print(list(result1))
print(list(result2))

