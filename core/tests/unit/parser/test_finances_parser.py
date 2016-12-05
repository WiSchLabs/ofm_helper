import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Finance
from core.parsers.finances_parser import FinancesParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class FinancesParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'finances.html'), encoding='utf8')
        self.matchday = MatchdayFactory.create()
        self.user = OFMUserFactory.create()
        self.parser = FinancesParser(testdata, self.user, self.matchday)
        self.finances = self.parser.parse()

    def test_finances_parser(self):
        self.assertEqual(type(self.finances), Finance)

        self.assertEqual('1633872', self.finances.balance)

        self.assertEqual('54450', self.finances.income_visitors_league)
        self.assertEqual('0', self.finances.income_sponsoring)
        self.assertEqual('0', self.finances.income_cup)
        self.assertEqual('20749', self.finances.income_interests)
        self.assertEqual('0', self.finances.income_loan)
        self.assertEqual('0', self.finances.income_transfer)
        self.assertEqual('0', self.finances.income_visitors_friendlies)
        self.assertEqual('30000', self.finances.income_friendlies)
        self.assertEqual('0', self.finances.income_funcup)
        self.assertEqual('0', self.finances.income_betting)

        self.assertEqual('167945', self.finances.expenses_player_salaries)
        self.assertEqual('432000', self.finances.expenses_stadium)
        self.assertEqual('8280', self.finances.expenses_youth)
        self.assertEqual('0', self.finances.expenses_interests)
        self.assertEqual('0', self.finances.expenses_trainings)
        self.assertEqual('0', self.finances.expenses_transfer)
        self.assertEqual('0', self.finances.expenses_compensation)
        self.assertEqual('0', self.finances.expenses_friendlies)
        self.assertEqual('0', self.finances.expenses_funcup)
        self.assertEqual('0', self.finances.expenses_betting)
