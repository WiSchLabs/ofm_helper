import os
from core.factories.core_factories import MatchdayFactory, SeasonFactory
from core.models import PlayerStatistics, Player, Matchday, Contract, Country
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from django.test import TestCase

from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class StatisticsParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'), encoding='utf8')
        MatchdayFactory.create()
        user = OFMUserFactory.create()
        season = SeasonFactory.create()

        country_choices = dict(Country._meta.get_field('country').choices)
        country_no_greece = list(country_choices.keys())[list(country_choices.values()).index('Griechenland')]
        nationality_greece, success = Country.objects.get_or_create(country=country_no_greece)

        self.player = Player.objects.create(id='159883060', position='TW', name='Chrístos Tsigas', birth_season=season, nationality=nationality_greece)
        self.player = Player.objects.create(id='160195494', position='LV', name='Irwin O\'Canny', birth_season=season, nationality=nationality_greece)
        self.player = Player.objects.create(id='159341445', position='LMD', name='Jan Stemmler', birth_season=season, nationality=nationality_greece)

        self.parser = PlayerStatisticsParser(testdata, user)
        self.player_stat_list = self.parser.parse()
        self.first_player_stat = self.player_stat_list[0]
        self.assertEqual(Matchday.objects.all().count(), 1)

    def test_parsed_player_stat_contains_all_foreign_keys(self):
        self.assertEquals(type(self.first_player_stat), PlayerStatistics)
        self.assertEquals(type(self.first_player_stat.player), Player)
        self.assertEquals(self.first_player_stat.matchday.number, 0)
        self.assertEquals(self.first_player_stat.matchday.season.number, 1)

    def test_parsed_player_stat_contains_all_fields(self):
        self.assertEquals(3, len(self.player_stat_list))
        self.assertEquals('TW', self.first_player_stat.player.position)
        self.assertEquals(159883060, self.first_player_stat.player.id)
        self.assertEquals('Chrístos Tsigas', self.first_player_stat.player.name)
        self.assertEquals('15', self.first_player_stat.strength)
        self.assertEquals('47', self.first_player_stat.freshness)
        self.assertEquals('29', self.first_player_stat.games_in_season)

    def test_parsed_player_stat_contains_correct_scored_goals(self):
        player_stat = self.player_stat_list[2]
        self.assertEquals('4', player_stat.goals_in_season)

    def test_parsed_player_stat_contains_correct_tacklings(self):
        self.assertEquals('32', self.first_player_stat.won_tacklings_in_season)
        self.assertEquals('36', self.first_player_stat.lost_tacklings_in_season)
        self.assertEquals('37', self.first_player_stat.won_friendly_tacklings_in_season)
        self.assertEquals('5', self.first_player_stat.lost_friendly_tacklings_in_season)

    def test_parsed_player_stat_contains_correct_cards_received(self):
        player_stat = self.player_stat_list[1]
        self.assertEquals('3', player_stat.yellow_cards_in_season)
        self.assertEquals('1', player_stat.red_cards_in_season)

    def test_parsed_player_stat_contains_correct_player_enhancement_data(self):
        self.assertEquals('8599', self.first_player_stat.ep)
        self.assertEquals('13227', self.first_player_stat.tp)
        self.assertEquals('10422', self.first_player_stat.awp)

    def test_parsed_player_stat_contains_correct_equity(self):
        self.assertEquals('16015782', self.first_player_stat.equity)

    def test_parse_player_stat_should_return_same_instance_if_nothing_changes(self):
        self.parser.html_source = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'), encoding='utf8')
        stat2 = self.parser.parse()
        self.assertEqual(self.player_stat_list, stat2)
        self.assertEquals(Player.objects.all().count(), 3)
        self.assertEqual(Matchday.objects.all().count(), 1)

    def test_parsed_contract_is_registered(self):
        self.assertEquals(Contract.objects.all().count(), 3)
