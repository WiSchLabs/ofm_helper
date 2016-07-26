from unittest.mock import Mock, patch

import core
import os
from core.factories.core_factories import MatchdayFactory
from core.models import PlayerStatistics, Player
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from django.core.urlresolvers import reverse
from django.test import TestCase
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class ParserViewTest(TestCase):
    def setUp(self):
        matchday = MatchdayFactory.create(season__number=100)
        self.user = OFMUser.objects.create_user('name', 'mail@pro.com', 'pass', ofm_username='name', ofm_password='pass')

        self.player = Player.objects.create(id='159883060', name='Chrístos Tsigas', birth_season=matchday.season)
        self.player = Player.objects.create(id='160195494', name='Irwin O\'Canny', birth_season=matchday.season)

        self.client.login(username='name', password='pass')

    @patch('core.views.SiteManager')
    def test_parser_view(self, site_manager_mock):
        with open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8') as matchday_html:
            with open(os.path.join(TESTDATA_PATH, 'player.html'), encoding='utf8') as player_html:
                with open(os.path.join(TESTDATA_PATH, 'frame_player_statistics.html'), encoding='utf8') as player_statistics_html:
                    mp = MatchdayParser(matchday_html.read())
                    pp = PlayersParser(player_html.read(), self.user)
                    psp = PlayerStatisticsParser(player_statistics_html.read(), self.user)

                    core.views.MatchdayParser = Mock(spec=mp)
                    core.views.MatchdayParser.return_value.parse = mp.parse

                    core.views.PlayersParser = Mock(spec=pp)
                    core.views.PlayersParser.return_value.parse = pp.parse

                    core.views.PlayerStatisticsParser = Mock(spec=psp)
                    core.views.PlayerStatisticsParser.return_value.parse = psp.parse

                    response = self.client.get(reverse('core:trigger_parsing'))
                    self.assertEqual(response.status_code, 302)

        # test player statistics parsing
        player_statistics = PlayerStatistics.objects.all()

        self.assertEquals(player_statistics.count(), 2)

        # test matchday parsing
        self.assertEquals(player_statistics[0].matchday.number, 23)
        self.assertEquals(player_statistics[0].matchday.season.number, 139)

        self.assertEquals(player_statistics[0].player.name, 'Chrístos Tsigas')
        self.assertEquals(player_statistics[0].strength, 15)

        self.assertEquals(player_statistics[1].player.name, "Irwin O'Canny")
        self.assertEquals(player_statistics[1].strength, 14)

        # test players parsing
        first_parsed_player = Player.objects.all()[2]

        self.assertEquals(22, Player.objects.all().count())
        self.assertEquals('Saliou Dassé', first_parsed_player.name)
        self.assertEquals('TW', first_parsed_player.position)
        self.assertEquals(163703532, first_parsed_player.id)
        self.assertEquals('Elfenbeinküste', str(first_parsed_player.nationality))
