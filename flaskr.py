import sys
import os
import json
from opencricket.config import config

from flask import Flask, request, abort, make_response

sys.path.append(os.path.dirname(__file__))

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.suggestion.productions import Productions
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

@app.route("/productions")
def production():
    r = make_response(Productions().productions())
    r.mimetype = 'application/json'
    return r

@app.route("/load_index")
def load_index():
    r = make_response(Productions().load_index(config.exploded_dir))
    r.mimetype = 'application/json'
    return r

@app.route("/create_index")
def load_index():
    Productions().load_index(config.exploded_dir)
    return ok()

@app.route("/ping")
def ping():
    return ok()

def ok():
    r = make_response(json.dumps({'status': 'ok'}))
    r.mimetype = 'application/json'
    return r

if __name__ == "__main__":
    app.run('127.0.0.1', 9001, debug=True)