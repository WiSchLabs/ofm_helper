import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Match, MatchTeamStatistics
from core.parsers.match_parser import MatchParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class MatchParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'home_match.html'), encoding='utf8')
        MatchdayFactory.create(number=1)
        self.user = OFMUserFactory.create()

        parser = MatchParser(testdata, self.user, True)
        self.match_stat = parser.parse()

    def test_match_parser_general_informations(self):
        self.assertEqual(type(self.match_stat), Match)
        self.assertEqual(self.match_stat.matchday.number, '8')
        self.assertEqual(self.match_stat.user, self.user)
        self.assertEqual(self.match_stat.match_type, 'L')
        self.assertEqual(self.match_stat.venue, 'Club-Mate-Arena')
        self.assertEqual(self.match_stat.is_in_future, False)

    def test_match_home_team_statistics(self):
        self.assertEqual(type(self.match_stat.home_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.home_team_statistics.score, '0')
        self.assertEqual(self.match_stat.home_team_statistics.team_name, 'BSC Wittenau')
        self.assertEqual(self.match_stat.home_team_statistics.strength, '40')
        self.assertEqual(self.match_stat.home_team_statistics.ball_possession, '37.4')
        self.assertEqual(self.match_stat.home_team_statistics.chances, '0')
        self.assertEqual(self.match_stat.home_team_statistics.yellow_cards, '0')
        self.assertEqual(self.match_stat.home_team_statistics.red_cards, '0')

    def test_match_guest_team_statistics(self):
        self.assertEqual(type(self.match_stat.guest_team_statistics), MatchTeamStatistics)
        self.assertEqual(self.match_stat.guest_team_statistics.score, '3')
        self.assertEqual(self.match_stat.guest_team_statistics.team_name, 'Ruhrorter SC')
        self.assertEqual(self.match_stat.guest_team_statistics.strength, '67')
        self.assertEqual(self.match_stat.guest_team_statistics.ball_possession, '62.6')
        self.assertEqual(self.match_stat.guest_team_statistics.chances, '4')
        self.assertEqual(self.match_stat.guest_team_statistics.yellow_cards, '0')
        self.assertEqual(self.match_stat.guest_team_statistics.red_cards, '0')

    def test_match_gets_updated_on_parsing_again(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'home_match_2.html'), encoding='utf8')

        parser = MatchParser(testdata, self.user, True)
        match_stat2 = parser.parse()

        self.assertEqual(self.match_stat.id, match_stat2.id)
        self.assertEqual(self.match_stat.home_team_statistics.id, match_stat2.home_team_statistics.id)
        self.assertEqual(self.match_stat.guest_team_statistics.id, match_stat2.guest_team_statistics.id)
        self.assertEqual(match_stat2.home_team_statistics.strength, '42')
        self.assertEqual(match_stat2.guest_team_statistics.strength, '69')
        self.assertEqual(2, MatchTeamStatistics.objects.all().count())
