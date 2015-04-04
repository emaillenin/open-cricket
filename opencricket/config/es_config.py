import logging
from elasticsearch import Elasticsearch

index_settings = '{  "settings": {    "index": {      "analysis": {        "filter": {          "stemmer": {            "type": "stemmer",            "language": "english"          },          "autocompleteFilter": {            "max_shingle_size": "5",            "min_shingle_size": "2",            "type": "shingle"          },          "stopwords": {            "type": "stop",            "stopwords": [              "_english_"            ]          }        },        "analyzer": {          "didYouMean": {            "filter": [              "lowercase"            ],            "type": "custom",            "tokenizer": "standard"          },          "autocomplete": {            "filter": [              "lowercase",              "autocompleteFilter"            ],            "type": "custom",            "tokenizer": "standard"          },          "default": {            "filter": [              "lowercase",              "stopwords",              "stemmer"            ],         "type": "custom",            "tokenizer": "standard"          }        }      }    }  }  }'

delete_documents = '{"query":{"match_all":{}}}'
def es_suggestion(search_string):
    return '{"suggest":{"didYouMean":{"text":"%s","phrase":{"field":"did_you_mean"}}},"query":{"match":{"question":"%s"}}}' % (search_string, search_string)

def type_mapping(doc_type):
    return '{  "%s": {    "properties": {      "autocomplete": {        "type": "string",        "analyzer": "autocomplete"      },      "did_you_mean": {        "type": "string",        "analyzer": "didYouMean"      },      "question": {        "type": "string",        "copy_to": [          "autocomplete",          "did_you_mean"        ]      }    }  }  }' % doc_type

def es_fuzzy_match(search_string):
    return '{"query":{"match":{"question":{"query":"%s","fuzziness":3,"prefix_length":2}}}}' % search_string


def es_builder(hosts=None):
    if (hosts == None): hosts = '127.0.0.1'
    logger = logging.getLogger('elasticsearch')
    logger.setLevel(logging.WARNING)
    return Elasticsearch(hosts=hosts, timeout=600, request_timeout=600)
