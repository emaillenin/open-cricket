import sys
import os
import json
from opencricket.config import config

from flask import Flask, request, abort, make_response

sys.path.append(os.path.dirname(__file__))

from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_response import SyntaxResponse
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
        print(str(e))
        abort(500)
    result = parser.parse_sentence()
    if result is not None:
        return SyntaxResponse.build_response(result, False)
    else:
        abort(422)

@app.route("/productions")
def production():
    r = make_response(Productions().productions())
    r.mimetype = 'application/json'
    return r


@app.route("/suggestions")
def suggestions():
    return json_response(Productions().suggestions(request.args.get('search', '')))

@app.route("/load_index")
def load_index():
    r = make_response(Productions().load_index(config.exploded_dir))
    r.mimetype = 'application/json'
    return r

@app.route("/create_index")
def create_index():
    Productions().create_index()
    return ok()

@app.route("/delete_index")
def delete_index():
    Productions().delete_index()
    return ok()

@app.route("/ping")
def ping():
    return ok()

def ok():
    return json_response({'status': 'ok'})

def json_response(dict_response):
    r = make_response(json.dumps(dict_response))
    r.mimetype = 'application/json'
    return r

if __name__ == "__main__":
    app.run('127.0.0.1', 9001, debug=True)