import os

from django.test import TestCase

from core.factories.match_related_core_factories import MatchFactory, MatchStadiumStatisticsFactory
from core.models import StadiumStandStatistics
from core.parsers.stadium_stand_statistics_parser import StadiumStandStatisticsParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class StadiumStandStatisticsParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'stadium_overview_special_construction_and_repair.html'),
                        encoding='utf8')
        self.user = OFMUserFactory.create(username='IsaacAsimov')
        self.match = MatchFactory.create(user=self.user)
        MatchStadiumStatisticsFactory.create(match=self.match)

        self.parser = StadiumStandStatisticsParser(testdata, self.user, self.match)
        self.stadium_stand_stats = self.parser.parse()

    def test_stadium_stand_stat_parser_north_stand_set_under_construction_after_match(self):
        self.assertEqual(type(self.stadium_stand_stats[0]), StadiumStandStatistics)
        self.assertEqual(self.stadium_stand_stats[0].sector, 'N')
        self.assertEqual(self.stadium_stand_stats[0].condition, 100)
        self.assertEqual(self.stadium_stand_stats[0].visitors, '200')
        self.assertEqual(self.stadium_stand_stats[0].ticket_price, '35')
        self.assertEqual(self.stadium_stand_stats[0].level.capacity, '200')
        self.assertEqual(self.stadium_stand_stats[0].level.has_roof, True)
        self.assertEqual(self.stadium_stand_stats[0].level.has_seats, True)

    def test_stadium_stand_stat_parser_east_set_under_construction_before_match(self):
        self.assertEqual(self.stadium_stand_stats[1], None)

    def test_stadium_stand_stat_parser_south_stand_set_in_repair_after_match(self):
        self.assertEqual(type(self.stadium_stand_stats[2]), StadiumStandStatistics)
        self.assertEqual(self.stadium_stand_stats[2].sector, 'S')
        self.assertEqual(self.stadium_stand_stats[2].condition, 100)
        self.assertEqual(self.stadium_stand_stats[2].visitors, '398')
        self.assertEqual(self.stadium_stand_stats[2].ticket_price, '35')
        self.assertEqual(self.stadium_stand_stats[2].level.capacity, '400')
        self.assertEqual(self.stadium_stand_stats[2].level.has_roof, True)
        self.assertEqual(self.stadium_stand_stats[2].level.has_seats, False)

    def test_stadium_stand_stat_parser_west_set_in_repair_before_match(self):
        self.assertEqual(self.stadium_stand_stats[3], None)
