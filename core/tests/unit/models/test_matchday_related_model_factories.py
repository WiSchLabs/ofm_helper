from django.test import TestCase

from core.factories.core_factories import FinanceFactory, MatchdayFactory, MatchFactory, \
                                          PlayerStatisticsFactory, QuarterFactory, SeasonFactory
from core.models import Matchday
from users.models import OFMUser


class CreateCoreModelsTest(TestCase):
    def test_create_season(self):
        s = SeasonFactory.create(number=2)
        self.assertIsNotNone(s)
        self.assertEqual(s.number, 2)

    def test_create_quarter(self):
        q = QuarterFactory.create()
        self.assertIsNotNone(q)
        self.assertEqual(q.season.number, 1)
        self.assertEqual(q.quarter, 1)

    def test_create_matchday(self):
        m = MatchdayFactory.create()
        self.assertIsNotNone(m)
        self.assertEqual(m.season.number, 1)
        self.assertEqual(m.number, 0)

    def test_get_current_matchday_default(self):
        MatchdayFactory.create(number=1)
        m2 = MatchdayFactory.create(number=5)
        self.assertEqual(Matchday.get_current(), m2)

    def test_get_current_matchday_from_finances(self):
        MatchdayFactory.create(number=1)
        m2 = MatchdayFactory.create(number=5)
        MatchdayFactory.create(number=15)
        FinanceFactory.create(matchday=m2)
        self.assertEqual(Matchday.get_current(), m2)

    def test_get_current_matchday_from_player_statistics(self):
        MatchdayFactory.create(number=1)
        m2 = MatchdayFactory.create(number=5)
        m3 = MatchdayFactory.create(number=7)
        MatchdayFactory.create(number=15)
        FinanceFactory.create(matchday=m2)
        PlayerStatisticsFactory.create(matchday=m3)
        self.assertEqual(Matchday.get_current(), m3)

    def test_get_current_matchday_from_matches(self):
        user2 = OFMUser.objects.create_user(
            username='second',
            email='second@ofmhelper.com',
            password='second',
            ofm_username="second",
            ofm_password="second"
        )
        MatchdayFactory.create(number=1)
        m2 = MatchdayFactory.create(number=5)
        m3 = MatchdayFactory.create(number=7)
        m4 = MatchdayFactory.create(number=9)
        MatchdayFactory.create(number=15)
        FinanceFactory.create(matchday=m2, user=user2)
        PlayerStatisticsFactory.create(matchday=m3)
        MatchFactory.create(matchday=m4, user=user2)
        self.assertEqual(Matchday.get_current(), m4)

    def test_matchday_order_desc_by_number(self):
        MatchdayFactory.create(number=1)
        MatchdayFactory.create(number=2)
        self.assertEqual(Matchday.objects.all()[0].number, 2)

    def test_matchday_order_desc_by_season(self):
        s = SeasonFactory.create(number=2)
        MatchdayFactory.create()
        MatchdayFactory.create(season=s)
        self.assertEqual(Matchday.objects.all()[0].season.number, 2)
