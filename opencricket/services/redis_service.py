import redis


class RedisService:
    def __init__(self, namespace='opencricket-syntax-cache'):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.namespace = namespace

    def clear_syntax(self):
        self.redis.delete(self.namespace)

    def add_syntax(self, key, syntax):
        self.redis.hset(self.namespace, key, syntax)

    def get_syntax(self, key):
        return self.redis.hget(self.namespace, key).decode()

    def get_syntax_list(self):
        return sorted(list(s.decode() for s in self.redis.hkeys(self.namespace)))