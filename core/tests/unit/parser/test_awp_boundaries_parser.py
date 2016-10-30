import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import AwpBoundaries
from core.parsers.awp_boundaries_parser import AwpBoundariesParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class AwpBoundariesParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'awp_boundaries.html'), encoding='utf8')
        self.matchday = MatchdayFactory.create()
        self.user = OFMUserFactory.create()
        self.parser = AwpBoundariesParser(testdata, self.user)
        self.awp_boundaries = self.parser.parse()

    def test_parser(self):
        self.assertEquals(type(self.awp_boundaries), AwpBoundaries)
        self.assertEquals(AwpBoundaries.objects.count(), 1)

        self.assertEquals(self.awp_boundaries[2], 113)
        self.assertEquals(self.awp_boundaries[3], 332)
        self.assertEquals(self.awp_boundaries[4], 569)
        self.assertEquals(self.awp_boundaries[5], 883)
        self.assertEquals(self.awp_boundaries[6], 1306)
        self.assertEquals(self.awp_boundaries[7], 1865)
        self.assertEquals(self.awp_boundaries[8], 2641)
        self.assertEquals(self.awp_boundaries[9], 3616)
        self.assertEquals(self.awp_boundaries[10], 4649)
        self.assertEquals(self.awp_boundaries[11], 5673)
        self.assertEquals(self.awp_boundaries[12], 6694)
        self.assertEquals(self.awp_boundaries[13], 7766)
        self.assertEquals(self.awp_boundaries[14], 8893)
        self.assertEquals(self.awp_boundaries[15], 10049)
        self.assertEquals(self.awp_boundaries[16], 11141)
        self.assertEquals(self.awp_boundaries[17], 12203)
        self.assertEquals(self.awp_boundaries[18], 13240)
        self.assertEquals(self.awp_boundaries[19], 14230)
        self.assertEquals(self.awp_boundaries[20], 15254)
        self.assertEquals(self.awp_boundaries[21], 16309)
        self.assertEquals(self.awp_boundaries[22], 17311)
        self.assertEquals(self.awp_boundaries[23], 18302)
        self.assertEquals(self.awp_boundaries[24], 18999)
        self.assertEquals(self.awp_boundaries[25], 20078)
        self.assertEquals(self.awp_boundaries[26], 20795)
        self.assertEquals(self.awp_boundaries[27], 21105)

    def test_parser_does_not_create_new_boundaries_object_if_already_exists_for_quarter(self):
        self.matchday = MatchdayFactory.create(number=2)
        self.parser = AwpBoundariesParser(open(os.path.join(TESTDATA_PATH, 'awp_boundaries.html'), encoding='utf8'), self.user)
        self.parser.parse()

        self.assertEquals(AwpBoundaries.objects.count(), 1)

    def test_parser_creates_new_boundaries_object(self):
        self.matchday = MatchdayFactory.create(number=17)
        self.parser = AwpBoundariesParser(open(os.path.join(TESTDATA_PATH, 'awp_boundaries.html'), encoding='utf8'), self.user)
        self.parser.parse()

        self.assertEquals(AwpBoundaries.objects.count(), 2)

