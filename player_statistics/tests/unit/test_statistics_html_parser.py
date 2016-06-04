from django.test import TestCase
import os

from player_statistics.parsers.player_statistics_html_parser import PlayerStatisticsHtmlParser

TESTDATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'assets')


class StatisticsHtmlParserTest(TestCase):
    def setUp(self):
        self.testdata = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'))

    def test_parser_can_parse_player_statistics(self):
        parser = PlayerStatisticsHtmlParser()
        soup = parser.parse(self.testdata)
        self.assertEqual('OFM Spielerstatistik', soup.title.string)
