from unittest.mock import Mock, patch

import core
import os
from core.factories.core_factories import MatchdayFactory
from core.models import PlayerStatistics, Country, Player
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class StatisticsParserViewTest(TestCase):
    def setUp(self):
        self.matchday = MatchdayFactory.create(season__number=100)
        self.user = OFMUser.objects.create_user('name', 'mail@pro.com', 'pass', ofm_username='name', ofm_password='pass')

        self.player = Player.objects.create(id='159883060', name='Chrístos Tsigas', birth_season=self.matchday.season)
        self.player = Player.objects.create(id='160195494', name='Irwin O\'Canny', birth_season=self.matchday.season)

        self.client.login(username='name', password='pass')

    @patch('core.views.SiteManager')
    def test_parser_view(self, site_manager_mock):
        with open(os.path.join(TESTDATA_PATH, 'frame_player_statistics.html'), encoding='utf8') as f:
            p = PlayerStatisticsParser(f.read(), self.user)

            core.views.PlayerStatisticsParser = Mock(spec=p)
            core.views.PlayerStatisticsParser.return_value.parse = p.parse

            response = self.client.get(reverse('core:trigger_player_statistics_parsing'))
            self.assertEqual(response.status_code, 302)

        player_statistics = PlayerStatistics.objects.all()

        self.assertEquals(player_statistics.count(), 2)

        self.assertEquals(player_statistics[0].matchday.number, 0)
        self.assertEquals(player_statistics[0].matchday.season.number, 100)

        self.assertEquals(player_statistics[0].player.name, 'Chrístos Tsigas')
        self.assertEquals(player_statistics[0].strength, 15)

        self.assertEquals(player_statistics[1].player.name, "Irwin O'Canny")
        self.assertEquals(player_statistics[1].strength, 14)

