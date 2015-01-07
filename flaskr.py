import sys
import os
from opencricket.config import config

from flask import Flask, request, abort

sys.path.append(os.path.dirname(__file__))

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.player_names import PlayerNames

app = Flask(__name__)


@app.route("/")
def search():
    try:
        user_search = request.args.get('search', '')
        player_names = PlayerNames(config.metadata_dir + 'player_names.txt').get_player_names(user_search)
        parser = SentenceParser(user_search, player_names)
    except Exception as e:
        print(e.__doc__)
        print(e.message)
        abort(500)
    result = parser.parse_sentence()
    if result is not None:
        return result
    else:
        abort(422)

@app.route("/ping")
def ping():
    return 'OK', 200


if __name__ == "__main__":
    app.run('127.0.0.1', 9090)