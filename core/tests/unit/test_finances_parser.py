import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Player, Contract, Finance
from core.parsers.finances_parser import FinancesParser
from core.parsers.players_parser import PlayersParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class PlayersParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'finances.html'), encoding='utf8')
        self.matchday = MatchdayFactory.create()
        self.user = OFMUserFactory.create()
        self.parser = FinancesParser(testdata, self.user)
        self.finances = self.parser.parse()

    def test_players_parser(self):
        self.assertEquals(type(self.finances), Finance)

        self.assertEquals('1633872', self.finances.balance)

        self.assertEquals('54450', self.finances.income_visitors_league)
        self.assertEquals('0', self.finances.income_sponsoring)
        self.assertEquals('0', self.finances.income_cup)
        self.assertEquals('20749', self.finances.income_interests)
        self.assertEquals('0', self.finances.income_loan)
        self.assertEquals('0', self.finances.income_transfer)
        self.assertEquals('0', self.finances.income_visitors_friendlies)
        self.assertEquals('30000', self.finances.income_friendlies)
        self.assertEquals('0', self.finances.income_funcup)
        self.assertEquals('0', self.finances.income_betting)

        self.assertEquals('167945', self.finances.expenses_player_salaries)
        self.assertEquals('432000', self.finances.expenses_stadium)
        self.assertEquals('8280', self.finances.expenses_youth)
        self.assertEquals('0', self.finances.expenses_interests)
        self.assertEquals('0', self.finances.expenses_trainings)
        self.assertEquals('0', self.finances.expenses_transfer)
        self.assertEquals('0', self.finances.expenses_compensation)
        self.assertEquals('0', self.finances.expenses_friendlies)
        self.assertEquals('0', self.finances.expenses_funcup)
        self.assertEquals('0', self.finances.expenses_betting)
