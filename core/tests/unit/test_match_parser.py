import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Match
from core.parsers.match_parser import MatchParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class MatchParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'home_match.html'), encoding='utf8')
        MatchdayFactory.create(number=1)
        self.user = OFMUserFactory.create()

        self.parser = MatchParser(testdata, self.user)
        self.match_stat = self.parser.parse()

    def test_match_parser(self):
        self.assertEquals(type(self.match_stat), Match)
        self.assertEquals(self.match_stat.matchday.number, 1)
        self.assertEquals(self.match_stat.user, self.user)
        self.assertEquals(self.match_stat.home_goals, '0')
        self.assertEquals(self.match_stat.guest_goals, '3')
        self.assertEquals(self.match_stat.venue, 'Club-Mate-Arena')
        self.assertEquals(self.match_stat.home_team, 'BSC Wittenau')
        self.assertEquals(self.match_stat.guest_team, 'HJK Tantrum')
        self.assertEquals(self.match_stat.match_type, 'L')
