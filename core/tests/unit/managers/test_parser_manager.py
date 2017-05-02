from unittest import TestCase, skip
from unittest.mock import patch

from core.factories.matchday_related_core_factories import MatchdayFactory
from core.managers.parser_manager import ParserManager


class ParserManagerTest(TestCase):
    def setUp(self):
        self.parser_manager = ParserManager()

    @patch('core.parsers.ofm_helper_version_parser.OfmHelperVersionParser.parse')
    def test_parse_ofm_version(self, parse_version_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_ofm_version(site_manager_mock)

        assert parse_version_mock.called

    @patch('core.parsers.matchday_parser.MatchdayParser.parse')
    def test_parse_matchday(self, parse_matchday_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_matchday(site_manager_mock)

        assert parse_matchday_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.parsers.players_parser.PlayersParser.parse')
    def test_parse_players_and_matchday(self, parse_players_mock, parse_matchday_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_players(site_manager_mock)

        assert parse_matchday_mock.called
        assert parse_players_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.parsers.player_statistics_parser.PlayerStatisticsParser.parse')
    def test_parse_player_statistics(self, parse_player_statistics_mock, parse_matchday_mock):
        self.parser_manager.players_already_parsed = True
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_player_statistics(site_manager_mock)

        assert not parse_matchday_mock.called
        assert parse_player_statistics_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_players')
    @patch('core.parsers.player_statistics_parser.PlayerStatisticsParser.parse')
    def test_parse_player_statistics_and_matchday(self, parse_player_statistics_mock, parse_players_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_player_statistics(site_manager_mock)

        assert parse_players_mock.called
        assert parse_player_statistics_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.parsers.awp_boundaries_parser.AwpBoundariesParser.parse')
    def test_parse_awp_and_matchday(self, parse_awp_mock, parse_matchday_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_awp_boundaries(site_manager_mock)

        assert parse_matchday_mock.called
        assert parse_awp_mock.called

    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    @patch('core.parsers.finances_parser.FinancesParser.parse')
    def test_parse_finances_and_matchday(self, parse_finances_mock, parse_matchday_mock):
        with patch('core.managers.site_manager.OFMSiteManager') as site_manager_mock:
            site_manager_mock.browser.page_source.return_value = "<html></html>"
            self.parser_manager.parse_finances(site_manager_mock)

        assert parse_matchday_mock.called
        assert parse_finances_mock.called

    @skip('Works locally, but not on travis...')
    @patch('core.managers.parser_manager.ParserManager._convert_transfer_data')
    @patch('core.managers.site_manager.OFMTransferSiteManager.kill_browser')
    @patch('core.managers.site_manager.OFMTransferSiteManager.download_transfer_excels')
    @patch('core.managers.parser_manager.ParserManager.parse_matchday')
    def test_parse_transfer_data(self, parse_matchday_mock, download_transfers_mock, kill_browser_mock, convert_mock):
        with patch('core.managers.site_manager.OFMTransferSiteManager') as site_manager_mock:
            site_manager_mock.download_transfer_excels = download_transfers_mock
            site_manager_mock._convert_transfer_data = convert_mock  # pylint: disable=protected-access
            site_manager_mock.kill_browser = kill_browser_mock
            self.parser_manager.parsed_matchday = MatchdayFactory.create()

            self.parser_manager.parse_transfers(site_manager_mock)

        assert download_transfers_mock.called
        assert kill_browser_mock.called
