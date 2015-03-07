import json


class SyntaxResponse:
    @staticmethod
    def build_response(syntax_string, suggested, suggested_search=None, did_you_mean=None):
        syntax_json = json.loads(syntax_string)
        response_json = {"root": list(syntax_json.keys())[0], "suggested": suggested}
        response_json.update(syntax_json)
        if suggested: response_json.update({"suggested_search": suggested_search})
        if did_you_mean is not None: response_json.update({"did_you_mean": did_you_mean})
        return response_json

    @staticmethod
    def build_did_you_mean_response(did_you_mean):
        return {"did_you_mean": did_you_mean}

    @staticmethod
    def build_related_search(related_search):
        return {"related_search": related_search}