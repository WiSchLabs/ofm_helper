from unittest import skip

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Player, PlayerStatistics
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager


class StatisticsParserTest(TestCase):
    def setUp(self):
        self.site_manager = SiteManager()
        self.site_manager.login()
        self.site_manager.browser.get(Constants.TEAM.PLAYER_STATISTICS)
        self.assertIn('Spielerstatistik', self.site_manager.browser.title)
        parser = PlayerStatisticsParser()
        parser.url = self.site_manager.browser.page_source
        MatchdayFactory.create()
        self.player_stat_list = parser.parse()
        self.first_player_stat = self.player_stat_list[0]

    @skip('because i say so, mindestens, digga')
    def test_parsed_player_stat_contains_all_foreign_keys(self):
        self.assertEquals(type(self.first_player_stat), PlayerStatistics)
        self.assertEquals(type(self.first_player_stat.player), Player)
