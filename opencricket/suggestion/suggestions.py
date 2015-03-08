from opencricket.config import es_config


class Suggestions:
    def __init__(self, es_host=None):
        self.es = es_config.es_builder(es_host)

    def suggestions(self, search_string):
        return self.es.search(index='opencricket', body=es_config.es_suggestion(search_string))

    def first_suggestion(self, search_string):
        suggestions = self.suggestions(search_string)
        hits = suggestions['hits']['hits']
        if len(hits) > 1 and hits[0]['_score'] > hits[1]['_score']:
            return hits[0]['_source']['question']
        else:
            return None

    def all_suggestions(self, search_string):
        suggestions = self.suggestions(search_string)
        hits = suggestions['hits']['hits']
        if len(hits) > 0:
            return [match['_source']['question'] for match in hits]
        else:
            return None

    def related_search(self, search_string):
        fuzzy_matches = self.es.search(index='opencricket', body=es_config.es_fuzzy_match(search_string))
        hits = fuzzy_matches['hits']['hits']
        if len(hits) > 0:
            return [match['_source']['question'] for match in hits]
        else:
            return None

    def did_you_mean(self, search_string):
        suggestions = self.suggestions(search_string)
        did_you_mean_options = suggestions['suggest']['didYouMean'][0]['options']
        if len(did_you_mean_options) > 0:
            return [dym['text'] for dym in did_you_mean_options]
        else:
            return None
