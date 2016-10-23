import os

from django.test import TestCase

from core.parsers.ofm_helper_version_parser import OfmHelperVersionParser

TESTDATA_PATH = 'core/tests/assets'


class MatchdayParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'GitHubRelease.html'), encoding='utf8')
        self.parser = OfmHelperVersionParser(testdata)

    def test_parse_ofm_helper_version(self):
        ofm_helper_version = self.parser.parse()
        self.assertEqual("v0.1.12", ofm_helper_version)
