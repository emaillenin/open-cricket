import json


class SyntaxResponse:
    @staticmethod
    def build_response(syntax_string, suggested):
        syntax_json = json.loads(syntax_string)
        response_json = {"root": list(syntax_json.keys())[0], "suggested": suggested}
        response_json.update(syntax_json)
        return json.dumps(response_json)
