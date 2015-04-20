import sys
import os
from opencricket.chart.syntax_cache import SyntaxCache

sys.path.append(os.path.dirname(__file__))

import json
from opencricket.config import config
from flask import Flask, request, abort, make_response
from opencricket.chart.sentence_parser import SentenceParser
from opencricket.chart.syntax_response import SyntaxResponse
from opencricket.suggestion.productions import Productions
from opencricket.suggestion.suggestions import Suggestions
from opencricket.chart.player_names import PlayerNames

app = Flask(__name__)


@app.route("/")
def search():
    user_search = request.args.get('search', '')
    try:
        player_names = PlayerNames(config.metadata_dir + 'player_names.txt').get_player_names(user_search)
        parser = SentenceParser(user_search, player_names)
    except Exception as e:
        print(e.__doc__, file=sys.stderr)
        print(str(e), file=sys.stderr)
        abort(500)
    result = parser.parse_sentence()
    if result is not None:
        all_suggestions = Suggestions().all_suggestions(user_search)
        return json_response(SyntaxResponse.build_response(result, False,related_searches=all_suggestions))
    else:
        first_suggestion = Suggestions().first_suggestion(user_search)
        if first_suggestion is not None:
            parser = SentenceParser(first_suggestion, player_names)
            did_you_mean = Suggestions().did_you_mean(user_search)
            return json_response(SyntaxResponse.build_response(parser.parse_sentence(), True, suggested_search=first_suggestion, did_you_mean=did_you_mean))
        else:
            all_suggestions = Suggestions().all_suggestions(user_search)
            if all_suggestions is not None:
                return json_response(SyntaxResponse.build_related_search(all_suggestions))
            else:
                did_you_mean = Suggestions().did_you_mean(user_search)
                if did_you_mean is not None:
                    return json_response(SyntaxResponse.build_did_you_mean_response(did_you_mean))
                else:
                    abort(422)

@app.route("/syntax_cache")
def syntax_cache():
    SyntaxCache().build_cache()
    return ok()

@app.route("/related")
def related():
    return json_response(SyntaxResponse.build_related_search(Suggestions().related_search(request.args.get('search',''))))

@app.route("/productions")
def production():
    return json_response(Productions().productions(config.expansions_dir))

@app.route("/suggestions")
def suggestions():
    return json_response(Suggestions().suggestions(request.args.get('search', '')))

@app.route("/load_index")
def load_index():
    Productions().load_index(config.exploded_dir)
    return ok()

@app.route("/create_index")
def create_index():
    Productions().create_index()
    return ok()

@app.route("/put_mapping")
def put_mapping():
    Productions().put_mapping(request.args.get('doc_type', 'player_stats'))
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
