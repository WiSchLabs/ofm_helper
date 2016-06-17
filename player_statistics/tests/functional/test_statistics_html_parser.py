from django.test import TestCase

from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager

from player_statistics.models import Player, PlayerStatistics
from player_statistics.parsers.player_statistics_html_parser import PlayerStatisticsHtmlParser


class StatisticsHtmlParserTest(TestCase):
    def setUp(self):
        self.site_manager = SiteManager()
    #    self.site_manager.login()
    #    self.site_manager.browser.get(Constants.TEAM.PLAYER_STATISTICS)
    #    parser = PlayerStatisticsHtmlParser()
    #    self.player_stat_list = parser.parse(self.site_manager.browser.page_source)
    #    self.first_player_stat = self.player_stat_list[0]

    #def test_parsed_player_stat_contains_all_foreign_keys(self):
    #    self.assertEquals(type(self.first_player_stat), PlayerStatistics)
    #    self.assertEquals(type(self.first_player_stat.player), Player)
