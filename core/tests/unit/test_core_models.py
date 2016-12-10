from django.test import TestCase

from core.factories.core_factories import SeasonFactory, QuarterFactory, MatchdayFactory, PlayerStatisticsFactory, \
    ContractFactory, PlayerFactory, CountryFactory, FinanceFactory, MatchFactory, MatchStadiumStatisticsFactory, \
    StadiumStandStatisticsFactory, MatchTeamStatisticsFactory, StandLevelFactory, StadiumLevelFactory, \
    StadiumLevelItemFactory, ChecklistFactory, ChecklistItemFactory
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

    def test_create_player_statistics(self):
        st = PlayerStatisticsFactory.create()
        self.assertEqual(st.ep, 2)
        self.assertEqual(st.tp, 5)
        self.assertEqual(st.awp, 3)
        self.assertEqual(st.strength, 1)
        self.assertEqual(st.freshness, 4)
        self.assertEqual(st.games_in_season, 0)
        self.assertEqual(st.goals_in_season, 0)
        self.assertEqual(st.won_tacklings_in_season, 0)
        self.assertEqual(st.lost_tacklings_in_season, 0)
        self.assertEqual(st.won_friendly_tacklings_in_season, 0)
        self.assertEqual(st.lost_friendly_tacklings_in_season, 0)
        self.assertEqual(st.yellow_cards_in_season, 0)
        self.assertEqual(st.red_cards_in_season, 0)
        self.assertEqual(st.equity, 0)

    def test_create_player(self):
        c = CountryFactory.create()
        p = PlayerFactory.create(position=1, name='tw1', nationality=c)
        self.assertIsNotNone(p)
        self.assertEqual(p.position, 1)
        self.assertEqual(p.name, 'tw1')
        self.assertTrue(p.nationality is not None)
        self.assertEqual(p.birth_season.number, 1)

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

    def test_create_match_team_statistics(self):
        mts = MatchTeamStatisticsFactory.create()
        self.assertEqual(mts.team_name, 'Springfield Isotopes')
        self.assertEqual(mts.score, 0)
        self.assertEqual(mts.strength, 50)
        self.assertEqual(mts.ball_possession, 50)
        self.assertEqual(mts.chances, 3)
        self.assertEqual(mts.yellow_cards, 2)
        self.assertEqual(mts.red_cards, 0)

    def test_create_match(self):
        m = MatchFactory.create()
        self.assertEqual(m.match_type, 'L')
        self.assertEqual(m.venue, 'Olympiastadion Berlin')
        self.assertFalse(m.is_won)
        self.assertTrue(m.is_draw)
        self.assertFalse(m.is_lost)
        self.assertFalse(m.is_in_future)

    def test_create_match_stadium_statistics(self):
        mss = MatchStadiumStatisticsFactory.create()
        self.assertTrue(mss.match is not None)
        self.assertTrue(mss.stand_statistics is not None)

    def test_create_stadium_level_item(self):
        sli = StadiumLevelItemFactory.create()
        self.assertEqual(sli.current_level, 0)
        self.assertEqual(sli.value, 0)
        self.assertEqual(sli.daily_costs, 0)

    def test_create_stadium_level(self):
        sl = StadiumLevelFactory.create()
        self.assertTrue(sl.light is not None)
        self.assertTrue(sl.screen is not None)
        self.assertTrue(sl.security is not None)
        self.assertTrue(sl.parking is not None)

    def test_create_stand_level(self):
        sl = StandLevelFactory.create()
        self.assertEqual(sl.capacity, 100)
        self.assertFalse(sl.has_roof)
        self.assertFalse(sl.has_seats)

    def test_create_stadium_stand_statistics(self):
        sss = StadiumStandStatisticsFactory.create()
        self.assertTrue(sss.stadium_statistics is not None)
        self.assertEqual(sss.sector, 'N')
        self.assertEqual(sss.visitors, 42)
        self.assertEqual(sss.ticket_price, 55)
        self.assertEqual(sss.condition, 99.42)

    def test_create_checklist(self):
        cl = ChecklistFactory.create()
        self.assertTrue(cl.user is not None)

    def test_create_checklist_item(self):
        cli = ChecklistItemFactory.create()
        self.assertTrue(cli.checklist is not None)
        self.assertEqual(cli.name, 'Item 1')
        self.assertTrue(cli.last_checked_on_matchday is None)
        self.assertTrue(cli.to_be_checked_on_matchdays is None)
        self.assertTrue(cli.to_be_checked_on_matchday_pattern is None)
        self.assertFalse(cli.to_be_checked_if_home_match_tomorrow)
