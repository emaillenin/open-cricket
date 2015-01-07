# To run this benchmark:
# goto the project root and: python benchmarks.py
from opencricket.chart.player_names import PlayerNames

import os

def benchmark_player_name_lookup():
    user_search = 'dhoni and virat kohli stats'
    PlayerNames(os.path.join(os.path.dirname(__file__), 'tests', 'data', 'player_names.txt')).get_player_names(user_search)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("benchmark_player_name_lookup()", setup="from __main__ import benchmark_player_name_lookup",  number=1500))