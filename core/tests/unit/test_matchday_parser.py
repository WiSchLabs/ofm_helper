import os

from django.test import TestCase

from core.parsers.matchday_parser import MatchdayParser

TESTDATA_PATH = 'core/tests/assets'


class MatchdayParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8')
        self.parser = MatchdayParser()
        self.parser.url = testdata

    def test_parse_matchday(self):
        matchday = self.parser.parse()
        self.assertEqual(139, matchday.season.number)
        self.assertEqual(23, matchday.number)

    def test_parse_matchday_should_return_same_instance_if_nothing_changes(self):
        matchday1 = self.parser.parse()
        self.parser.url = open(os.path.join(TESTDATA_PATH, 'head.html'), encoding='utf8')
        matchday2 = self.parser.parse()
        self.assertEqual(matchday1.number, matchday2.number)
        self.assertEqual(matchday1.season.number, matchday2.season.number)
        self.assertEqual(matchday1, matchday2)
