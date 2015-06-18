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
from opencricket.config import es_config

app = Flask(__name__)
SyntaxCache().build_cache()
app.config.from_object('environment.' + (os.environ.get('OPENCRICKET_ENV') or 'Development'))

@app.route("/")
def search():
    user_search = request.args.get('search', '')
    elastic_search = es_connection()

    try:
        player_names = PlayerNames(config.metadata_dir + 'player_names.txt').get_player_names(user_search)
        parser = SentenceParser(user_search, player_names)
    except Exception as e:
        print(e.__doc__, file=sys.stderr)
        print(str(e), file=sys.stderr)
        abort(500)
    result = parser.parse_sentence()
    if result is not None:
        all_suggestions = Suggestions(elastic_search).all_suggestions(user_search)
        return json_response(SyntaxResponse.build_response(result, False,related_searches=all_suggestions))
    else:
        first_suggestion = Suggestions(elastic_search).first_suggestion(user_search)
        if first_suggestion is not None:
            parser = SentenceParser(first_suggestion, player_names)
            did_you_mean = Suggestions(elastic_search).did_you_mean(user_search)
            return json_response(SyntaxResponse.build_response(parser.parse_sentence(), True, suggested_search=first_suggestion, did_you_mean=did_you_mean))
        else:
            all_suggestions = Suggestions(elastic_search).all_suggestions(user_search)
            if all_suggestions is not None:
                return json_response(SyntaxResponse.build_related_search(all_suggestions))
            else:
                did_you_mean = Suggestions(elastic_search).did_you_mean(user_search)
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
    return json_response(SyntaxResponse.build_related_search(Suggestions(es_connection()).related_search(request.args.get('search',''))))

@app.route("/productions")
def production():
    return json_response(Productions(es_connection()).productions(config.expansions_dir))

@app.route("/explosions")
def explode():
    json_response(Productions(es_connection()).explode(config.expansions_dir, config.exploded_dir))
    return ok()

@app.route("/suggestions")
def suggestions():
    return json_response(Suggestions(es_connection()).suggestions(request.args.get('search', '')))

@app.route("/load_index")
def load_index():
    Productions(es_connection()).load_index(config.exploded_dir)
    return ok()

@app.route("/create_index")
def create_index():
    Productions(es_connection()).create_index()
    return ok()

@app.route("/put_mapping")
def put_mapping():
    Productions(es_connection()).put_mapping(request.args.get('doc_type', 'player_stats'))
    return ok()

@app.route("/delete_index")
def delete_index():
    Productions(es_connection()).delete_index()
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


def es_connection():
    return es_config.es_builder(port=app.config.get('ELASTICSEARCH_PORT'))

if __name__ == "__main__":
    app.run('127.0.0.1', 9001, debug=app.config.get('DEBUG'))
