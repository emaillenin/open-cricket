class Environment(object):
    DEBUG = False

class Development(Environment):
    DEBUG = True
    ELASTICSEARCH_PORT = 9200

class Test(Environment):
    ELASTICSEARCH_PORT = 9200

class Production(Environment):
    ELASTICSEARCH_PORT = 9200
