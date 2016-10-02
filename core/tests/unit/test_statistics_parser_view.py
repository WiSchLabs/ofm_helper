from unittest.mock import Mock, patch

from bs4 import BeautifulSoup

import core
import os
from core.factories.core_factories import MatchdayFactory
from core.models import PlayerStatistics, Player, Finance, Match, AwpBoundaries, AwpBoundariesKeyVal
from core.parsers.awp_boundaries_parser import AwpBoundariesParser
from core.parsers.finances_parser import FinancesParser
from core.parsers.match_parser import MatchParser
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
    @patch('core.views.BeautifulSoup')
    def test_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8') as matchday_html:
            with open(os.path.join(TESTDATA_PATH, 'player.html'), encoding='utf8') as player_html:
                with open(os.path.join(TESTDATA_PATH, 'frame_player_statistics.html'), encoding='utf8') as player_statistics_html:
                    with open(os.path.join(TESTDATA_PATH, 'awp_boundaries.html'), encoding='utf8') as awp_boundaries_html:
                        with open(os.path.join(TESTDATA_PATH, 'finances.html'), encoding='utf8') as finances_html:
                            with open(os.path.join(TESTDATA_PATH, 'home_match.html'), encoding='utf8') as match_html:
                                mdp = MatchdayParser(matchday_html.read())
                                pp = PlayersParser(player_html.read(), self.user)
                                psp = PlayerStatisticsParser(player_statistics_html.read(), self.user)
                                abp = AwpBoundariesParser(awp_boundaries_html.read(), self.user)
                                fp = FinancesParser(finances_html.read(), self.user)
                                mp = MatchParser(match_html.read(), self.user, True)

                                core.views.MatchdayParser = Mock(spec=mdp)
                                core.views.MatchdayParser.return_value.parse = mdp.parse

                                core.views.PlayersParser = Mock(spec=pp)
                                core.views.PlayersParser.return_value.parse = pp.parse

                                core.views.PlayerStatisticsParser = Mock(spec=psp)
                                core.views.PlayerStatisticsParser.return_value.parse = psp.parse

                                core.views.AwpBoundariesParser = Mock(spec=abp)
                                core.views.AwpBoundariesParser.return_value.parse = abp.parse

                                core.views.FinancesParser = Mock(spec=fp)
                                core.views.FinancesParser.return_value.parse = fp.parse

                                core.views.MatchParser = Mock(spec=mp)
                                core.views.MatchParser.return_value.parse = mp.parse

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

        # test awp boundaries parsing
        self.assertEquals(AwpBoundariesKeyVal.objects.filter(strength=2)[0].awp, 128)
        self.assertEquals(AwpBoundariesKeyVal.objects.filter(strength=3)[0].awp, 348)

        # test players parsing
        first_parsed_player = Player.objects.all()[2]

        self.assertEquals(22, Player.objects.all().count())
        self.assertEquals('Saliou Dassé', first_parsed_player.name)
        self.assertEquals('TW', first_parsed_player.position)
        self.assertEquals(163703532, first_parsed_player.id)
        self.assertEquals('Elfenbeinküste', str(first_parsed_player.nationality))

        # test finances
        self.assertEquals(1, Finance.objects.all().count())
        finance = Finance.objects.all()[0]
        self.assertEquals(1633872, finance.balance)

        # test match
        # TODO
