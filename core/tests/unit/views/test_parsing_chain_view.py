import os
from unittest.mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import ParsingSetting
from users.models import OFMUser

TESTDATA_PATH = 'core/tests/assets'


class ParserChainViewTest(TestCase):
    def setUp(self):
        MatchdayFactory.create(season__number=100, number=1)

        self.user = OFMUser.objects.create_user(
            username='name',
            email='',
            password='pass',
            ofm_username='name',
            ofm_password='pass'
        )
        self.client.login(username='name', password='pass')

    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view(self, site_manager_mock, parse_matchday_mock, parse_players_mock, parse_player_statistics_mock,  # pylint: disable=too-many-arguments
                         parse_finances_mock, parse_all_matches_mock, parse_awp_mock, parse_version_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)

        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        assert parse_finances_mock.called
        assert parse_all_matches_mock.called
        assert parse_awp_mock.called
        assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view_do_not_parse_player_statistics(self, site_manager_mock, parse_matchday_mock,  # pylint: disable=too-many-arguments
                                                        parse_players_mock, parse_player_statistics_mock,
                                                        parse_finances_mock, parse_all_matches_mock, parse_awp_mock,
                                                        parse_version_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = False
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = True
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = False
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)

        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert not parse_players_mock.called
        assert not parse_player_statistics_mock.called
        assert parse_finances_mock.called
        assert parse_all_matches_mock.called
        assert parse_awp_mock.called
        assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view_do_not_parse_finances(self, site_manager_mock, parse_matchday_mock, parse_players_mock,  # pylint: disable=too-many-arguments
                                               parse_player_statistics_mock, parse_finances_mock,
                                               parse_all_matches_mock, parse_awp_mock, parse_version_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = False
        parsing_setting.parsing_chain_includes_matches = True
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = False
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)

        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        assert not parse_finances_mock.called
        assert parse_all_matches_mock.called
        assert parse_awp_mock.called
        assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager._parse_match_details')
    @patch('core.managers.parser_manager.ParserManager._parse_stadium_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view_do_not_parse_matches(self, site_manager_mock, parse_matchday_mock, parse_players_mock,  # pylint: disable=too-many-arguments
                                              parse_player_statistics_mock, parse_finances_mock,
                                              parse_all_matches_mock, parse_awp_mock, parse_version_mock,
                                              parse_stadium_statistics_mock, parse_match_details_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = True
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = False
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = False
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)

        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        assert parse_finances_mock.called
        assert not parse_all_matches_mock.called
        assert not parse_match_details_mock.called
        assert not parse_stadium_statistics_mock.called
        assert parse_awp_mock.called
        assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view_do_not_parse_awp_boundaries(self, site_manager_mock, parse_matchday_mock, parse_players_mock,  # pylint: disable=too-many-arguments
                                                     parse_player_statistics_mock, parse_finances_mock,
                                                     parse_all_matches_mock, parse_awp_mock, parse_version_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
        parsing_setting.parsing_chain_includes_player_statistics = True
        parsing_setting.parsing_chain_includes_awp_boundaries = False
        parsing_setting.parsing_chain_includes_finances = True
        parsing_setting.parsing_chain_includes_matches = True
        parsing_setting.parsing_chain_includes_match_details = True
        parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = False
        parsing_setting.parsing_chain_includes_stadium_details = True
        parsing_setting.save()
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)

        assert site_manager_mock.called
        assert parse_matchday_mock.called
        assert parse_players_mock.called
        assert parse_player_statistics_mock.called
        assert parse_finances_mock.called
        assert parse_all_matches_mock.called
        assert not parse_awp_mock.called
        assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager._parse_match_details')
    @patch('core.managers.parser_manager.ParserManager._parse_stadium_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    def test_parser_view_do_not_parse_stadium_statistics(self, parse_matchday_mock,  # pylint: disable=too-many-arguments
                                                         parse_players_mock, parse_player_statistics_mock,
                                                         parse_finances_mock, parse_awp_mock,
                                                         parse_version_mock, parse_stadium_statistics_mock,
                                                         parse_match_details_mock):

        with open(os.path.join(TESTDATA_PATH, 'match_schedule.html'), encoding='utf8') as match_schedule_html:
            with patch('core.views.trigger_parsing_views.SiteManager') as site_manager_mock:
                site_manager_instance_mock = site_manager_mock.return_value
                site_manager_instance_mock.browser.page_source = match_schedule_html
                site_manager_instance_mock.user = self.user
                parsing_setting, _ = ParsingSetting.objects.get_or_create(user=self.user)
                parsing_setting.parsing_chain_includes_player_statistics = True
                parsing_setting.parsing_chain_includes_awp_boundaries = True
                parsing_setting.parsing_chain_includes_finances = True
                parsing_setting.parsing_chain_includes_matches = True
                parsing_setting.parsing_chain_includes_match_details = True
                parsing_setting.parsing_chain_includes_match_details_only_for_current_matchday = False
                parsing_setting.parsing_chain_includes_stadium_details = False
                parsing_setting.save()
                response = self.client.get(reverse('core:trigger:trigger_parsing'))

                self.assertEqual(response.status_code, 302)

                assert site_manager_mock.called
                assert parse_matchday_mock.called
                assert parse_players_mock.called
                assert parse_player_statistics_mock.called
                assert parse_finances_mock.called
                assert parse_match_details_mock.called
                assert not parse_stadium_statistics_mock.called
                assert parse_awp_mock.called
                assert parse_version_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_ofm_version')
    @patch('core.managers.parser_manager.ParserManager.parse_awp_boundaries')
    @patch('core.managers.parser_manager.ParserManager.parse_all_matches')
    @patch('core.managers.parser_manager.ParserManager.parse_finances')
    @patch('core.managers.parser_manager.ParserManager.parse_player_statistics')
    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.views.trigger_parsing_views.SiteManager')
    def test_parser_view_not_callable_if_logged_out(self, site_manager_mock, parse_matchday_mock, parse_players_mock,  # pylint: disable=too-many-arguments
                                                    parse_player_statistics_mock, parse_finances_mock,
                                                    parse_all_matches_mock, parse_awp_mock, parse_version_mock):
        site_manager_instance_mock = site_manager_mock.return_value
        site_manager_instance_mock.user = self.user
        self.client.get(reverse('core:account:logout'))
        response = self.client.get(reverse('core:trigger:trigger_parsing'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:account:login'))

        assert not site_manager_mock.called
        assert not parse_matchday_mock.called
        assert not parse_players_mock.called
        assert not parse_player_statistics_mock.called
        assert not parse_finances_mock.called
        assert not parse_all_matches_mock.called
        assert not parse_awp_mock.called
        assert not parse_version_mock.called
