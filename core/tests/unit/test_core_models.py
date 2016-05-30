import unittest

from core.factories.core_factories import SeasonFactory, QuarterFactory


class CreateCoreModelsTest(unittest.TestCase):
    def test_create_season(self):
        s = SeasonFactory.create(season=2)
        self.assertIsNotNone(s)
        self.assertEquals(s.season, 2)

    def test_create_quarter(self):
        q = QuarterFactory.create()
        self.assertIsNotNone(q)
        self.assertEquals(q.season.season, 1)
        self.assertEquals(q.quarter, 1)

if __name__ == '__main__':
    unittest.main()
