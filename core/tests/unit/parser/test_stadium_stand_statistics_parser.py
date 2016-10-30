import os

from django.test import TestCase

from core.factories.core_factories import MatchStadiumStatisticsFactory, MatchFactory
from core.models import StadiumStandStatistics
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class StadiumStandStatisticsParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'stadium_overview.html'), encoding='utf8')
        self.user = OFMUserFactory.create(username='GeorgeOrwell')
        self.match = MatchFactory.create(user=self.user)
        MatchStadiumStatisticsFactory.create(match=self.match)

        self.parser = StadiumStandStatisticsParser(testdata, self.user)
        self.stadium_stand_stats = self.parser.parse()

    def test_stadium_stand_stat_parser_north_stand(self):
        self.assertEquals(type(self.stadium_stand_stats[0]), StadiumStandStatistics)
        self.assertEquals(self.stadium_stand_stats[0].sector, 'N')
        self.assertEquals(self.stadium_stand_stats[0].condition, '91.41')
        self.assertEquals(self.stadium_stand_stats[0].visitors, '97')
        self.assertEquals(self.stadium_stand_stats[0].ticket_price, '35')
        self.assertEquals(self.stadium_stand_stats[0].level.capacity, '200')
        self.assertEquals(self.stadium_stand_stats[0].level.has_roof, False)
        self.assertEquals(self.stadium_stand_stats[0].level.has_seats, True)

    def test_stadium_stand_stat_parser_east_stand(self):
        self.assertEquals(type(self.stadium_stand_stats[1]), StadiumStandStatistics)
        self.assertEquals(self.stadium_stand_stats[1].sector, 'O')
        self.assertEquals(self.stadium_stand_stats[1].condition, '94.02')
        self.assertEquals(self.stadium_stand_stats[1].visitors, '99')
        self.assertEquals(self.stadium_stand_stats[1].ticket_price, '20')
        self.assertEquals(self.stadium_stand_stats[1].level.capacity, '100')
        self.assertEquals(self.stadium_stand_stats[1].level.has_roof, False)
        self.assertEquals(self.stadium_stand_stats[1].level.has_seats, False)

    def test_stadium_stand_stat_parser_south_stand(self):
        self.assertEquals(type(self.stadium_stand_stats[2]), StadiumStandStatistics)
        self.assertEquals(self.stadium_stand_stats[2].sector, 'S')
        self.assertEquals(self.stadium_stand_stats[2].condition, '50.86')
        self.assertEquals(self.stadium_stand_stats[2].visitors, '88')
        self.assertEquals(self.stadium_stand_stats[2].ticket_price, '35')
        self.assertEquals(self.stadium_stand_stats[2].level.capacity, '100')
        self.assertEquals(self.stadium_stand_stats[2].level.has_roof, True)
        self.assertEquals(self.stadium_stand_stats[2].level.has_seats, False)

    def test_stadium_stand_stat_parser_west_stand(self):
        self.assertEquals(type(self.stadium_stand_stats[3]), StadiumStandStatistics)
        self.assertEquals(self.stadium_stand_stats[3].sector, 'W')
        self.assertEquals(self.stadium_stand_stats[3].condition, '94.02')
        self.assertEquals(self.stadium_stand_stats[3].visitors, '99')
        self.assertEquals(self.stadium_stand_stats[3].ticket_price, '40')
        self.assertEquals(self.stadium_stand_stats[3].level.capacity, '100')
        self.assertEquals(self.stadium_stand_stats[3].level.has_roof, True)
        self.assertEquals(self.stadium_stand_stats[3].level.has_seats, True)
