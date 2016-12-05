import os

from bs4 import BeautifulSoup
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Match, MatchTeamStatistics
from core.parsers.won_by_default_match_row_parser import WonByDefaultMatchRowParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class WonByDefaultMatchRowParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'home_match_row_won_by_default.html'), encoding='utf8')
        MatchdayFactory.create(number=1)
        self.user = OFMUserFactory.create()

        soup = BeautifulSoup(testdata, "html.parser")

        self.parser = WonByDefaultMatchRowParser(soup, self.user)
        self.match_stat = self.parser.parse()

    def test_match_parser_general_informations(self):
        self.assertEqual(type(self.match_stat), Match)
        self.assertEqual(self.match_stat.matchday.number, '8')
        self.assertEqual(self.match_stat.user, self.user)
        self.assertEqual(self.match_stat.match_type, 'L')
        self.assertEqual(self.match_stat.venue, '')
        self.assertEqual(self.match_stat.is_in_future, False)

    def test_match_home_team_statistics(self):
        self.assertEqual(type(self.match_stat.home_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.home_team_statistics.score, '3')
        self.assertEqual(self.match_stat.home_team_statistics.team_name, 'BSC Wittenau')
        self.assertEqual(self.match_stat.home_team_statistics.strength, '58')
        self.assertEqual(self.match_stat.home_team_statistics.ball_possession, 100)
        self.assertEqual(self.match_stat.home_team_statistics.chances, 0)
        self.assertEqual(self.match_stat.home_team_statistics.yellow_cards, 0)
        self.assertEqual(self.match_stat.home_team_statistics.red_cards, 0)

    def test_match_guest_team_statistics(self):
        self.assertEqual(type(self.match_stat.guest_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.guest_team_statistics.score, '0')
        self.assertEqual(self.match_stat.guest_team_statistics.team_name, 'NicNock')
        self.assertEqual(self.match_stat.guest_team_statistics.strength, '0')
        self.assertEqual(self.match_stat.guest_team_statistics.ball_possession, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.chances, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.yellow_cards, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.red_cards, 0)

    def test_match_gets_updated_on_parsing_again(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'home_match_row_won_by_default_2.html'), encoding='utf8')

        soup = BeautifulSoup(testdata, "html.parser")

        self.parser = WonByDefaultMatchRowParser(soup, self.user)
        match_stat2 = self.parser.parse()

        self.assertEqual(self.match_stat.id, match_stat2.id)
        self.assertEqual(self.match_stat.home_team_statistics.id, match_stat2.home_team_statistics.id)
        self.assertEqual(self.match_stat.guest_team_statistics.id, match_stat2.guest_team_statistics.id)
        self.assertEqual(match_stat2.home_team_statistics.strength, '66')
        self.assertEqual(match_stat2.guest_team_statistics.strength, '1')
        self.assertEqual(2, MatchTeamStatistics.objects.all().count())
