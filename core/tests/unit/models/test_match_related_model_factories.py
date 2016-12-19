from django.test import TestCase

from core.factories.core_factories import MatchFactory, MatchStadiumStatisticsFactory, MatchTeamStatisticsFactory, \
                                          StadiumLevelFactory, StadiumLevelItemFactory, \
                                          StadiumStandStatisticsFactory, StandLevelFactory


class CreateCoreModelsTest(TestCase):
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
