from django.test import TestCase

from core.factories.core_factories import ChecklistFactory, ChecklistItemFactory, FinanceFactory, ParsingSettingFactory


class CoreModelFactoriesTest(TestCase):
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
        self.assertTrue(cli.is_inversed)

    def test_create_parsing_setting(self):
        ps = ParsingSettingFactory.create()
        self.assertTrue(ps.user is not None)
        self.assertTrue(ps.parsing_chain_includes_player_statistics)
        self.assertTrue(ps.parsing_chain_includes_awp_boundaries)
        self.assertTrue(ps.parsing_chain_includes_finances)
        self.assertTrue(ps.parsing_chain_includes_matches)
        self.assertFalse(ps.parsing_chain_includes_match_details)
        self.assertFalse(ps.parsing_chain_includes_stadium_details)
