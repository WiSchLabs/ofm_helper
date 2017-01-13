import os

from bs4 import BeautifulSoup
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Match, MatchTeamStatistics
from core.parsers.basic_match_row_parser import BasicMatchRowParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class FutureMatchRowParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'future_match_row.html'), encoding='utf8')
        MatchdayFactory.create(number=1)
        self.user = OFMUserFactory.create()

        soup = BeautifulSoup(testdata, "html.parser")

        parser = BasicMatchRowParser(soup, self.user)
        self.match_stat = parser.parse()

    def test_match_parser_general_informations(self):
        self.assertEqual(type(self.match_stat), Match)
        self.assertEqual(self.match_stat.matchday.number, '34')
        self.assertEqual(self.match_stat.user, self.user)
        self.assertEqual(self.match_stat.match_type, 'L')
        self.assertEqual(self.match_stat.venue, '')
        self.assertEqual(self.match_stat.is_in_future, True)

    def test_match_home_team_statistics(self):
        self.assertEqual(type(self.match_stat.home_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.home_team_statistics.score, 0)
        self.assertEqual(self.match_stat.home_team_statistics.team_name, 'BSC Wittenau')
        self.assertEqual(self.match_stat.home_team_statistics.strength, '60')
        self.assertEqual(self.match_stat.home_team_statistics.ball_possession, 0)
        self.assertEqual(self.match_stat.home_team_statistics.chances, 0)
        self.assertEqual(self.match_stat.home_team_statistics.yellow_cards, 0)
        self.assertEqual(self.match_stat.home_team_statistics.red_cards, 0)

    def test_match_guest_team_statistics(self):
        self.assertEqual(type(self.match_stat.guest_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.guest_team_statistics.score, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.team_name, 'Supporters Kiel')
        self.assertEqual(self.match_stat.guest_team_statistics.strength, '28')
        self.assertEqual(self.match_stat.guest_team_statistics.ball_possession, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.chances, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.yellow_cards, 0)
        self.assertEqual(self.match_stat.guest_team_statistics.red_cards, 0)

    def test_match_gets_updated_on_parsing_again(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'future_match_row_2.html'), encoding='utf8')

        soup = BeautifulSoup(testdata, "html.parser")

        parser = BasicMatchRowParser(soup, self.user)
        match_stat2 = parser.parse()

        self.assertEqual(self.match_stat.id, match_stat2.id)
        self.assertEqual(self.match_stat.home_team_statistics.id, match_stat2.home_team_statistics.id)
        self.assertEqual(self.match_stat.guest_team_statistics.id, match_stat2.guest_team_statistics.id)
        self.assertEqual(match_stat2.home_team_statistics.strength, '61')
        self.assertEqual(match_stat2.guest_team_statistics.strength, '29')
        self.assertEqual(2, MatchTeamStatistics.objects.all().count())
