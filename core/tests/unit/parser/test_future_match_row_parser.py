import os

from bs4 import BeautifulSoup
from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Match, MatchTeamStatistics
from core.parsers.future_match_row_parser import FutureMatchRowParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class FutureMatchRowParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'future_match_row.html'), encoding='utf8')
        MatchdayFactory.create(number=1)
        self.user = OFMUserFactory.create()

        soup = BeautifulSoup(testdata, "html.parser")

        self.parser = FutureMatchRowParser(soup, self.user)
        self.match_stat = self.parser.parse()

    def test_match_parser_general_informations(self):
        self.assertEquals(type(self.match_stat), Match)
        self.assertEquals(self.match_stat.matchday.number, '34')
        self.assertEquals(self.match_stat.user, self.user)
        self.assertEquals(self.match_stat.match_type, 'L')
        self.assertEquals(self.match_stat.venue, '')
        self.assertEquals(self.match_stat.is_scheduled, True)

    def test_match_home_team_statistics(self):
        self.assertEquals(type(self.match_stat.home_team_statistics), MatchTeamStatistics)
        self.assertEquals(self.match_stat.home_team_statistics.score, 0)
        self.assertEquals(self.match_stat.home_team_statistics.team_name, 'BSC Wittenau')
        self.assertEquals(self.match_stat.home_team_statistics.strength, '60')
        self.assertEquals(self.match_stat.home_team_statistics.ball_possession, 0)
        self.assertEquals(self.match_stat.home_team_statistics.chances, 0)
        self.assertEquals(self.match_stat.home_team_statistics.yellow_cards, 0)
        self.assertEquals(self.match_stat.home_team_statistics.red_cards, 0)

    def test_match_guest_team_statistics(self):
        self.assertEquals(type(self.match_stat.guest_team_statistics), MatchTeamStatistics)
        self.assertEquals(self.match_stat.guest_team_statistics.score, 0)
        self.assertEquals(self.match_stat.guest_team_statistics.team_name, 'Supporters Kiel')
        self.assertEquals(self.match_stat.guest_team_statistics.strength, '28')
        self.assertEquals(self.match_stat.guest_team_statistics.ball_possession, 0)
        self.assertEquals(self.match_stat.guest_team_statistics.chances, 0)
        self.assertEquals(self.match_stat.guest_team_statistics.yellow_cards, 0)
        self.assertEquals(self.match_stat.guest_team_statistics.red_cards, 0)
