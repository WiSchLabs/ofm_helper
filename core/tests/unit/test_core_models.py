from django.test import TestCase

from core.factories.core_factories import SeasonFactory, QuarterFactory, MatchdayFactory
from core.models import Matchday


class CreateCoreModelsTest(TestCase):
    def test_create_season(self):
        s = SeasonFactory.create(number=2)
        self.assertIsNotNone(s)
        self.assertEquals(s.number, 2)

    def test_create_quarter(self):
        q = QuarterFactory.create()
        self.assertIsNotNone(q)
        self.assertEquals(q.season.number, 1)
        self.assertEquals(q.quarter, 1)

    def test_create_matchday(self):
        m = MatchdayFactory.create()
        self.assertIsNotNone(m)
        self.assertEquals(m.season.number, 1)
        self.assertEquals(m.number, 1)

    def test_matchday_order_desc_by_number(self):
        MatchdayFactory.create(number=1)
        MatchdayFactory.create(number=2)
        self.assertEquals(Matchday.objects.all()[0].number, 2)

    def test_matchday_order_desc_by_season(self):
        s = SeasonFactory.create(number=2)
        MatchdayFactory.create()
        MatchdayFactory.create(season=s)
        self.assertEquals(Matchday.objects.all()[0].season.number, 2)

