from flask import Flask, request, abort

from chart.sentence_parser import SentenceParser

app = Flask(__name__)


@app.route("/")
def search():
    try:
        parser = SentenceParser(request.args.get('search', ''))
    except Exception as e:
        print e.__doc__
        print e.message
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