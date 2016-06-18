import os

from django.test import TestCase

from core.parsers.matchday_parser import MatchdayParser

TESTDATA_PATH = 'core/tests/assets'


class MatchdayParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8')
        parser = MatchdayParser()
        parser.url = testdata
        self.matchday = parser.parse()

    def test_parse_matchday(self):
        self.assertEqual(139, self.matchday.season.number)
        self.assertEqual(23, self.matchday.number)
