import os

from django.test import TestCase

from core.factories.core_factories import MatchFactory
from core.models import MatchStadiumStatistics, StadiumLevel, StadiumLevelItem, Match
from core.parsers.stadium_statistics_parser import StadiumStatisticsParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class StadiumStatisticsParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'stadium_environment.html'), encoding='utf8')
        self.user = OFMUserFactory.create(username='DouglasAdams')
        MatchFactory.create(user=self.user)

        self.parser = StadiumStatisticsParser(testdata, self.user)
        self.stadium_stat = self.parser.parse()

    def test_stadium_environment_parser_contains_correct_types(self):
        self.assertEquals(type(self.stadium_stat), MatchStadiumStatistics)
        self.assertEquals(type(self.stadium_stat.match), Match)
        self.assertEquals(type(self.stadium_stat.level), StadiumLevel)
        self.assertEquals(type(self.stadium_stat.level.light), StadiumLevelItem)
        self.assertEquals(type(self.stadium_stat.level.screen), StadiumLevelItem)
        self.assertEquals(type(self.stadium_stat.level.security), StadiumLevelItem)
        self.assertEquals(type(self.stadium_stat.level.parking), StadiumLevelItem)

    def test_stadium_environment_parser_contains_correct_light_data(self):
        self.assertEquals(self.stadium_stat.level.light.current_level, '1')
        self.assertEquals(self.stadium_stat.level.light.value, '20')
        self.assertEquals(self.stadium_stat.level.light.daily_costs, '10')

    def test_stadium_environment_parser_contains_correct_screen_data(self):
        self.assertEquals(self.stadium_stat.level.screen.current_level, '0')
        self.assertEquals(self.stadium_stat.level.screen.value, '0')
        self.assertEquals(self.stadium_stat.level.screen.daily_costs, '0')

    def test_stadium_environment_parser_contains_correct_security_data(self):
        self.assertEquals(self.stadium_stat.level.security.current_level, '2')
        self.assertEquals(self.stadium_stat.level.security.value, '200')
        self.assertEquals(self.stadium_stat.level.security.daily_costs, '150')

    def test_stadium_environment_parser_contains_correct_parking_data(self):
        self.assertEquals(self.stadium_stat.level.parking.current_level, '3')
        self.assertEquals(self.stadium_stat.level.parking.value, '42')
        self.assertEquals(self.stadium_stat.level.parking.daily_costs, '42')
