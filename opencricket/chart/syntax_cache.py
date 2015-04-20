from importlib import import_module
from opencricket.services.redis_service import RedisService
import os
import glob


class SyntaxCache:

    @staticmethod
    def build_cache():
        redis_service = RedisService()
        redis_service.clear_syntax()
        modules = glob.glob(os.path.dirname(__file__)+"/strategies/*.py")
        __all__ = [ os.path.basename(f)[:-3] for f in modules]
        __all__.remove('__init__')
        for x in __all__:
            module = import_module('opencricket.chart.strategies.%s' % x)
            syntax_method = getattr(module, 'syntax')
            redis_service.add_syntax(x, syntax_method())



