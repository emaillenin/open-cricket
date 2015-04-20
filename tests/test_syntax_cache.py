from unittest import TestCase
from opencricket.chart.syntax_cache import SyntaxCache
from opencricket.services.redis_service import RedisService


class TestSyntaxCache(TestCase):

    def setUp(self):
        self.rs = RedisService()

    def test_build_cache(self):
        SyntaxCache.build_cache()
        self.assertTrue(self.rs.get_syntax_list() == ['compare', 'matches', 'matches_cond', 'most_x', 'partnerships', 'player_dismissals', 'player_stats', 'scores'])