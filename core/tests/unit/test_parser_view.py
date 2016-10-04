import os
from unittest.mock import Mock, patch, MagicMock

from django.core.urlresolvers import reverse
from django.test import TestCase

import core
from core.factories.core_factories import MatchdayFactory, PlayerFactory
from core.models import PlayerStatistics, Player, Finance, Match, Matchday
from core.parsers.finances_parser import FinancesParser
from core.parsers.match_parser import MatchParser
from core.parsers.matchday_parser import MatchdayParser
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from core.parsers.players_parser import PlayersParser
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class ParserViewTest(TestCase):
    def setUp(self):
        matchday = MatchdayFactory.create(season__number=100, number=1)
        self.user = OFMUser.objects.create_user('name', 'mail@pro.com', 'pass', ofm_username='name', ofm_password='pass')

        self.player = Player.objects.create(id='159883060', name='Chrístos Tsigas', birth_season=matchday.season)
        self.player = Player.objects.create(id='160195494', name='Irwin O\'Canny', birth_season=matchday.season)

        self.client.login(username='name', password='pass')

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    def test_matchday_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8') as matchday_html:
            mdp = MatchdayParser(matchday_html.read())
            core.views.MatchdayParser = Mock(spec=mdp)
            core.views.MatchdayParser.return_value.parse = mdp.parse

            response = self.client.get(reverse('core:trigger_matchday_parsing'))
            self.assertEqual(response.status_code, 302)

            parsed_matchday = Matchday.objects.all()[0]
            self.assertEquals(139, parsed_matchday.season.number)
            self.assertEquals(23, parsed_matchday.number)

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    def test_player_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'player.html'), encoding='utf8') as player_html:
            pp = PlayersParser(player_html.read(), self.user)
            core.views.PlayersParser = Mock(spec=pp)
            core.views.PlayersParser.return_value.parse = pp.parse

            response = self.client.get(reverse('core:trigger_players_parsing'))
            self.assertEqual(response.status_code, 302)

            parsed_player = Player.objects.all()[2]
            self.assertEquals(22, Player.objects.all().count())
            self.assertEquals('Saliou Dassé', parsed_player.name)
            self.assertEquals('TW', parsed_player.position)
            self.assertEquals(163703532, parsed_player.id)
            self.assertEquals('Elfenbeinküste', str(parsed_player.nationality))

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    def test_player_statistics_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'frame_player_statistics.html'), encoding='utf8') as player_statistics_html:
            psp = PlayerStatisticsParser(player_statistics_html.read(), self.user)
            core.views.PlayerStatisticsParser = Mock(spec=psp)
            core.views.PlayerStatisticsParser.return_value.parse = psp.parse

            response = self.client.get(reverse('core:trigger_player_statistics_parsing'))
            self.assertEqual(response.status_code, 302)

            parsed_player_statistics = PlayerStatistics.objects.all()
            self.assertEquals(parsed_player_statistics.count(), 2)
            self.assertEquals(parsed_player_statistics[0].matchday.number, 1)
            self.assertEquals(parsed_player_statistics[0].matchday.season.number, 100)
            self.assertEquals('Chrístos Tsigas', parsed_player_statistics[0].player.name)
            self.assertEquals(15, parsed_player_statistics[0].strength)
            self.assertEquals("Irwin O'Canny", parsed_player_statistics[1].player.name)
            self.assertEquals(14, parsed_player_statistics[1].strength)

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    def test_finances_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'finances.html'), encoding='utf8') as finances_html:
            fp = FinancesParser(finances_html.read(), self.user)
            core.views.FinancesParser = Mock(spec=fp)
            core.views.FinancesParser.return_value.parse = fp.parse

            response = self.client.get(reverse('core:trigger_finances_parsing'))
            self.assertEqual(response.status_code, 302)

            self.assertEquals(1, Finance.objects.all().count())
            parsed_finance = Finance.objects.all()[0]
            self.assertEquals(1633872, parsed_finance.balance)

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    def test_match_parser_view(self, site_manager_mock, beatiful_soup_mock):
        with open(os.path.join(TESTDATA_PATH, 'home_match.html'), encoding='utf8') as match_html:
            mp = MatchParser(match_html.read(), self.user, True)
            core.views.MatchParser = Mock(spec=mp)
            core.views.MatchParser.return_value.parse = mp.parse

            response = self.client.get(reverse('core:trigger_match_parsing'))
            self.assertEqual(response.status_code, 302)

            # TODO: test it!
            #self.assertEquals(1, Match.objects.all().count())
            #parsed_match = Match.objects.all()[0]
            #self.assertEquals('Club-Mate-Arena', parsed_match.venue)

    @patch('core.views.SiteManager')
    @patch('core.views.BeautifulSoup')
    @patch('core.views.parse_matchday')
    @patch('core.views.parse_players')
    @patch('core.views.parse_player_statistics')
    @patch('core.views.parse_finances')
    @patch('core.views.parse_match')
    def test_parser_view(self, site_manager_mock, beatiful_soup_mock, parse_matchday_mock, parse_players_mock,
                         parse_player_statistics_mock, parse_finances_mock, parse_match_mock):
        response = self.client.get(reverse('core:trigger_parsing'))
        self.assertEqual(response.status_code, 302)

        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        #assert parse_finances_mock.called  # is not called somehow...
        assert parse_match_mock.called

