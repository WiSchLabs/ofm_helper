import os
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

import core
from core.factories.core_factories import MatchdayFactory
from core.models import ParsingSetting
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class ParserViewTest(TestCase):
    def setUp(self):
        MatchdayFactory.create(season__number=100, number=1)

        self.user = OFMUser.objects.create_user(
            username='name',
            email='',
            password='pass',
            ofm_username='name',
            ofm_password='pass'
        )
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = True
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        self.client.login(username='name', password='pass')

    @patch('core.managers.parser_manager.MatchdayParser.parse')
    @patch('core.views.trigger_parsing_views.OFMSiteManager')
    def test_matchday_parser_view(self, site_manager_mock, matchday_parser_mock):
        response = self.client.get(reverse('core:trigger:trigger_matchday_parsing'))

        self.assertEqual(response.status_code, 302)

        assert core.views.trigger_parsing_views.OFMSiteManager.called
        assert matchday_parser_mock.called

    @patch('core.managers.parser_manager.PlayersParser.parse')
    @patch('core.managers.parser_manager.MatchdayParser.parse')
    @patch('core.views.trigger_parsing_views.OFMSiteManager')
    def test_player_parser_view(self, site_manager_mock, matchday_parser_mock, players_parser_mock):
        response = self.client.get(reverse('core:trigger:trigger_players_parsing'))

        self.assertEqual(response.status_code, 302)

        assert core.views.trigger_parsing_views.OFMSiteManager.called
        assert matchday_parser_mock.called
        assert players_parser_mock.called

    @patch('core.managers.parser_manager.PlayerStatisticsParser.parse')
    @patch('core.managers.parser_manager.PlayersParser.parse')
    @patch('core.managers.parser_manager.MatchdayParser.parse')
    @patch('core.views.trigger_parsing_views.OFMSiteManager')
    def test_player_statistics_parser_view(self, site_manager_mock, matchday_parser_mock, player_parser_mock,
                                           player_statistics_parser_mock):
        response = self.client.get(reverse('core:trigger:trigger_player_statistics_parsing'))

        self.assertEqual(response.status_code, 302)

        assert core.views.trigger_parsing_views.OFMSiteManager.called
        assert matchday_parser_mock.called
        assert player_parser_mock.called
        assert player_statistics_parser_mock.called

    @patch('core.managers.parser_manager.FinancesParser.parse')
    @patch('core.managers.parser_manager.MatchdayParser.parse')
    @patch('core.views.trigger_parsing_views.OFMSiteManager')
    def test_finances_parser_view(self, site_manager_mock, matchday_parser_mock, finances_parser_mock):
        response = self.client.get(reverse('core:trigger:trigger_finances_parsing'))

        self.assertEqual(response.status_code, 302)

        assert core.views.trigger_parsing_views.OFMSiteManager.called
        assert matchday_parser_mock.called
        assert finances_parser_mock.called

    @patch('core.managers.parser_manager.ParserManager._is_current_matchday')
    @patch('core.managers.parser_manager.ParserManager.parse_stadium_statistics')
    @patch('core.managers.parser_manager.MatchDetailsParser.parse')
    @patch('core.managers.parser_manager.MatchdayParser.parse')
    def test_match_details_parser_view(self, matchday_parser_mock, match_details_parser_mock,
                                       parse_stadium_statistics_mock, is_current_matchday_mock):
        with open(os.path.join(TESTDATA_PATH, 'match_schedule.html'), encoding='utf8') as match_schedule_html:
            with patch('core.views.trigger_parsing_views.OFMSiteManager') as site_manager_mock:
                site_manager_instance_mock = site_manager_mock.return_value
                site_manager_instance_mock.browser.page_source = match_schedule_html
                site_manager_instance_mock.user = self.user
                is_current_matchday_mock.return_value = True

                response = self.client.get(reverse('core:trigger:trigger_match_parsing'))

                self.assertEqual(response.status_code, 302)

                assert matchday_parser_mock.called
                assert match_details_parser_mock.called
                assert parse_stadium_statistics_mock.called

    @patch('core.managers.parser_manager.MatchdayParser.parse')
    @patch('core.views.trigger_parsing_views.OFMSiteManager')
    def test_matchday_parser_view_not_callable_if_not_logged_in(self, site_manager_mock, matchday_parser_mock):
        self.client.get(reverse('core:account:logout'))
        response = self.client.get(reverse('core:trigger:trigger_matchday_parsing'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))

        assert not core.views.trigger_parsing_views.OFMSiteManager.called
        assert not matchday_parser_mock.called
