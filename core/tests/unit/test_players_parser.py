import os

from django.test import TestCase

from core.factories.core_factories import MatchdayFactory
from core.models import Player, Contract
from core.parsers.players_parser import PlayersParser
from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class PlayersParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'player.html'), encoding='utf8')
        self.matchday = MatchdayFactory.create()
        self.user = OFMUserFactory.create()
        self.parser = PlayersParser(testdata, self.user)
        self.player_list = self.parser.parse()
        self.first_player = self.player_list[0]

    def test_players_parser(self):
        self.assertEquals(type(self.first_player), Player)
        self.assertEquals(20, len(self.player_list))
        self.assertEquals(20, Player.objects.all().count())

    def test_parsed_player_contains_all_fields(self):
        self.assertEquals('Igor Vernon', self.first_player.name)
        self.assertEquals('TW', self.first_player.position)
        self.assertEquals('163739266', self.first_player.id)
        self.assertEquals(29, self.matchday.season.number - self.first_player.birth_season.number)
        self.assertEquals('Frankreich', str(self.first_player.nationality))

    def test_parsed_player_has_ownership_by_user(self):
        self.assertEquals(1, len(Contract.objects.filter(player=self.first_player, user=self.user, sold_on_matchday=None)))
