from django.test import TestCase

from core.factories.core_factories import SeasonFactory, QuarterFactory, MatchdayFactory, PlayerStatisticsFactory, \
    ContractFactory, PlayerFactory, CountryFactory, FinanceFactory, MatchFactory, MatchStadiumStatisticsFactory, \
    StadiumStandStatisticsFactory
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
        self.assertEquals(st.ep, 2)
        self.assertEquals(st.tp, 5)
        self.assertEquals(st.awp, 3)
        self.assertEquals(st.strength, 1)
        self.assertEquals(st.freshness, 4)
        self.assertEquals(st.games_in_season, 0)
        self.assertEquals(st.goals_in_season, 0)
        self.assertEquals(st.won_tacklings_in_season, 0)
        self.assertEquals(st.lost_tacklings_in_season, 0)
        self.assertEquals(st.won_friendly_tacklings_in_season, 0)
        self.assertEquals(st.lost_friendly_tacklings_in_season, 0)
        self.assertEquals(st.yellow_cards_in_season, 0)
        self.assertEquals(st.red_cards_in_season, 0)
        self.assertEquals(st.equity, 0)

    def test_create_player(self):
        c = CountryFactory.create()
        p = PlayerFactory.create(position=1, name='tw1', nationality=c)
        self.assertIsNotNone(p)
        self.assertEquals(p.position, 1)
        self.assertEquals(p.name, 'tw1')
        self.assertTrue(p.nationality is not None)
        self.assertEquals(p.birth_season.number, 1)

    def test_create_contract(self):
        c = ContractFactory.create()
        self.assertTrue(c.player is not None)
        self.assertTrue(c.user is not None)
        self.assertTrue(c.bought_on_matchday is not None)
        self.assertTrue(c.sold_on_matchday is None)

    def test_create_country(self):
        c = CountryFactory.create()
        self.assertTrue(c.country is not None)

    def test_create_finance(self):
        f = FinanceFactory.create()
        self.assertTrue(f.user is not None)
        self.assertTrue(f.matchday is not None)

        self.assertEqual(f.balance, 1000)
        self.assertEqual(f.income_visitors_league, 100)
        self.assertEqual(f.income_sponsoring, 0)
        self.assertEqual(f.income_cup, 0)
        self.assertEqual(f.income_interests, 0)
        self.assertEqual(f.income_loan, 0)
        self.assertEqual(f.income_transfer, 0)
        self.assertEqual(f.income_visitors_friendlies, 0)
        self.assertEqual(f.income_friendlies, 0)
        self.assertEqual(f.income_funcup, 0)
        self.assertEqual(f.income_betting, 0)
        self.assertEqual(f.expenses_player_salaries, 100)
        self.assertEqual(f.expenses_stadium, 0)
        self.assertEqual(f.expenses_youth, 0)
        self.assertEqual(f.expenses_interests, 0)
        self.assertEqual(f.expenses_trainings, 0)
        self.assertEqual(f.expenses_transfer, 0)
        self.assertEqual(f.expenses_compensation, 0)
        self.assertEqual(f.expenses_friendlies, 0)
        self.assertEqual(f.expenses_funcup, 0)
        self.assertEqual(f.expenses_betting, 0)

    def test_create_match(self):
        m = MatchFactory.create()
        self.assertEqual(m.home_team, '1. SC Wedding')
        self.assertEqual(m.guest_team, 'BSC Wittenau')
        self.assertEqual(m.home_goals, 42)
        self.assertEqual(m.guest_goals, 0)
        self.assertEqual(m.match_type, 'L')
        self.assertEqual(m.venue, 'Olympiastadion Berlin')

    def test_create_match_stadium_statistics(self):
        mss = MatchStadiumStatisticsFactory.create()
        self.assertTrue(mss.match is not None)
        self.assertTrue(mss.stand_statistics is not None)

    def test_create_stadium_stand_statistics(self):
        sss = StadiumStandStatisticsFactory.create()
        self.assertTrue(sss.stadium_statistics is not None)
        self.assertEqual(sss.sector, 'N')
        self.assertEqual(sss.capacity, 100)
        self.assertEqual(sss.visitors, 42)
        self.assertEqual(sss.ticket_price, 55)
        self.assertEqual(sss.condition, 99.42)


