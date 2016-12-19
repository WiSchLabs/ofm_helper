from django.test import TestCase

from core.factories.core_factories import ContractFactory, CountryFactory, PlayerStatisticsFactory, PlayerFactory


class CreateCoreModelsTest(TestCase):
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
