import os
from unittest.mock import Mock, patch

from django.core.urlresolvers import reverse
from django.test import TestCase

import core
from core.factories.core_factories import MatchdayFactory
from core.models import PlayerStatistics, Player, Finance, Matchday
from core.parsers.finances_parser import FinancesParser
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
    @patch('core.managers.parser_manager.MatchdayParser')
    def test_matchday_parser_view(self, site_manager_mock, matchday_parser_mock):
        response = self.client.get(reverse('core:trigger_matchday_parsing'))
        self.assertEqual(response.status_code, 302)

        assert core.views.SiteManager.called
        assert core.managers.parser_manager.MatchdayParser.return_value.parse.called

    @patch('core.views.SiteManager')
    @patch('core.managers.parser_manager.PlayersParser')
    def test_player_parser_view(self, site_manager_mock, players_parser_mock):
        response = self.client.get(reverse('core:trigger_players_parsing'))
        self.assertEqual(response.status_code, 302)

        assert core.managers.parser_manager.PlayersParser.return_value.parse.called
        assert core.views.SiteManager.called

    @patch('core.views.SiteManager')
    @patch('core.managers.parser_manager.PlayerStatisticsParser')
    def test_player_statistics_parser_view(self, site_manager_mock, player_statistics_parser_mock):
        response = self.client.get(reverse('core:trigger_player_statistics_parsing'))
        self.assertEqual(response.status_code, 302)

        assert core.managers.parser_manager.PlayerStatisticsParser.return_value.parse.called
        assert core.views.SiteManager.called

    @patch('core.views.SiteManager')
    @patch('core.managers.parser_manager.FinancesParser')
    def test_finances_parser_view(self, site_manager_mock, finances_parser_mock):
        response = self.client.get(reverse('core:trigger_finances_parsing'))
        self.assertEqual(response.status_code, 302)

        assert core.managers.parser_manager.FinancesParser.return_value.parse.called
        assert core.views.SiteManager.called

    @patch('core.managers.parser_manager.MatchParser')
    @patch('core.managers.parser_manager.parse_stadium_statistics')
    def test_match_parser_view(self, _, parse_stadium_statistics_mock):
        with open(os.path.join(TESTDATA_PATH, 'matchday_table.html'), encoding='utf8') as matchday_table:
            with patch('core.views.SiteManager') as site_manager_mock:
                site_manager_instance_mock = site_manager_mock.return_value
                site_manager_instance_mock.browser.page_source = matchday_table

                response = self.client.get(reverse('core:trigger_match_parsing'))
                self.assertEqual(response.status_code, 302)

                assert core.managers.parser_manager.MatchParser.return_value.parse.called
                assert parse_stadium_statistics_mock.called

    @patch('core.views.SiteManager')
    @patch('core.managers.parser_manager.parse_matchday')
    @patch('core.managers.parser_manager.parse_players')
    @patch('core.managers.parser_manager.parse_player_statistics')
    @patch('core.managers.parser_manager.parse_finances')
    @patch('core.managers.parser_manager.parse_match')
    @patch('core.managers.parser_manager.parse_awp_boundaries')
    @patch('core.views.parse_ofm_version')
    def test_parser_view(self, site_manager_mock, parse_matchday_mock, parse_players_mock, parse_player_statistics_mock,
                         parse_finances_mock, parse_match_mock, parse_awp_mock, parse_version_mock):
        response = self.client.get(reverse('core:trigger_parsing'))

        self.assertEqual(response.status_code, 302)
        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        assert parse_finances_mock.called
        assert parse_match_mock.called
        assert parse_awp_mock.called
        assert parse_version_mock.called

