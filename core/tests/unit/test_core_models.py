from django.test import TestCase

from core.factories.core_factories import SeasonFactory, QuarterFactory


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