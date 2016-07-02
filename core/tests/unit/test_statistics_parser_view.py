from unittest.mock import Mock

import core
import os
from core.configuration_provider import ConfigurationProvider
from core.factories.core_factories import MatchdayFactory
from core.models import PlayerStatistics
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class StatisticsParserViewTest(TestCase):
    def setUp(self):
        MatchdayFactory.create(season__number=100)

        config = ConfigurationProvider()
        ofm_username = config.get('credentials', 'OFM_USERNAME')
        ofm_password = config.get('credentials', 'OFM_PASSWORD')
        OFMUser.objects.create_user('name', 'mail@pro.com', 'pass', ofm_username=ofm_username, ofm_password=ofm_password)

        self.client.login(username='name', password='pass')

    def test_parser_view(self):
        with open(os.path.join(TESTDATA_PATH, 'frame_player_statistics.html'), encoding='utf8') as f:
            p = PlayerStatisticsParser(f.read())

            core.views.PlayerStatisticsParser = Mock(spec=p)
            core.views.PlayerStatisticsParser.return_value.parse = p.parse

            response = self.client.get(reverse('core:trigger_player_statistics_parsing'))
            self.assertEqual(response.status_code, 302)

        player_statistics = PlayerStatistics.objects.all()

        self.assertEquals(player_statistics.count(), 12)
        self.assertEquals(player_statistics.count(), 12)

        self.assertEquals(player_statistics[0].matchday.number, 0)
        self.assertEquals(player_statistics[0].matchday.season.number, 100)

        self.assertEquals(player_statistics[0].player.name, 'Chrístos Tsigas')
        self.assertEquals(player_statistics[0].age, 34)
        self.assertEquals(player_statistics[0].strength, 15)
