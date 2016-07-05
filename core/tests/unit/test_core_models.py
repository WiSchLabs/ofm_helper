from django.test import TestCase

from core.factories.core_factories import SeasonFactory, QuarterFactory, MatchdayFactory, PlayerStatisticsFactory, \
    PlayerUserOwnershipFactory
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
        self.assertEquals(m.number, 0)

    def test_matchday_order_desc_by_number(self):
        MatchdayFactory.create(number=1)
        MatchdayFactory.create(number=2)
        self.assertEquals(Matchday.objects.all()[0].number, 2)

    def test_matchday_order_desc_by_season(self):
        s = SeasonFactory.create(number=2)
        MatchdayFactory.create()
        MatchdayFactory.create(season=s)
        self.assertEquals(Matchday.objects.all()[0].season.number, 2)

    def test_create_player_statistics(self):
        st = PlayerStatisticsFactory.create()
        self.assertEquals(st.ep, 0)
        self.assertEquals(st.tp, 0)
        self.assertEquals(st.awp, 0)
        self.assertEquals(st.strength, 1)
        self.assertEquals(st.freshness, 0)
        self.assertEquals(st.games_in_season, 0)
        self.assertEquals(st.goals_in_season, 0)
        self.assertEquals(st.won_tacklings_in_season, 0)
        self.assertEquals(st.lost_tacklings_in_season, 0)
        self.assertEquals(st.won_friendly_tacklings_in_season, 0)
        self.assertEquals(st.lost_friendly_tacklings_in_season, 0)
        self.assertEquals(st.yellow_cards_in_season, 0)
        self.assertEquals(st.red_cards_in_season, 0)
        self.assertEquals(st.equity, 0)

    def test_create_player_user_ownership(self):
        puo = PlayerUserOwnershipFactory.create()
        self.assertTrue(puo.player is not None)
        self.assertTrue(puo.user is not None)
        self.assertTrue(puo.boughtOnMatchday is not None)
        self.assertTrue(puo.soldOnMatchday is None)


