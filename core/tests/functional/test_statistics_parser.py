from unittest import skip

from core.configuration_provider import ConfigurationProvider
from django.test import TestCase, Client

from core.factories.core_factories import MatchdayFactory
from core.models import Player, PlayerStatistics
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.web.ofm_page_constants import Constants
from core.web.site_manager import SiteManager
from users.models import OFMUser


class StatisticsParserTest(TestCase):
    def setUp(self):
        config = ConfigurationProvider()
        ofm_username = config.get('credentials', 'OFM_USERNAME')
        ofm_password = config.get('credentials', 'OFM_PASSWORD')
        OFMUser('name', 'mail@pro.com', 'pass', ofm_username=ofm_username, ofm_password=ofm_password).create()

        self.client.login(username='name', password='pass')

        response = self.client.get('/account')
        self.assertEqual(response.status_code, 200)

        #self.assertIn('Spielerstatistik', self.site_manager.browser.title)
        #parser = PlayerStatisticsParser()
        #parser.url = self.site_manager.browser.page_source
        #MatchdayFactory.create()
        #self.player_stat_list = parser.parse()
        #self.first_player_stat = self.player_stat_list[0]

    @skip('because i say so, mindestens, digga')
    def test_parsed_player_stat_contains_all_foreign_keys(self):
        self.assertEquals(type(self.first_player_stat), PlayerStatistics)
        self.assertEquals(type(self.first_player_stat.player), Player)
