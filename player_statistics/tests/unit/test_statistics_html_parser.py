import os

from django.test import TestCase

from player_statistics.models import Player, PlayerStatistics
from player_statistics.parsers.player_statistics_html_parser import PlayerStatisticsHtmlParser

TESTDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'assets')


class StatisticsHtmlParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'))
        parser = PlayerStatisticsHtmlParser()
        self.player_stat_list = parser.parse(testdata)

    def test_parser_returns_list_of_player_statistics(self):
        self.assertEquals(type(self.player_stat_list), list)
        self.assertEquals(type(self.player_stat_list[0]), PlayerStatistics)

    def test_parsed_player_stat_has_player(self):
        first_player = self.player_stat_list[0].player
        self.assertEquals(type(first_player), Player)

    def test_parsed_player_stat_contains_correct_player_pos(self):
        first_player = self.player_stat_list[0].player
        self.assertEquals('TW', first_player.position)
