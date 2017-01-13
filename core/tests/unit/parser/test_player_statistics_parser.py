import os

from core.factories.matchday_related_core_factories import MatchdayFactory
from core.factories.matchday_related_core_factories import SeasonFactory
from core.models import PlayerStatistics, Player, Matchday, Contract, Country
from core.parsers.player_statistics_parser import PlayerStatisticsParser
from django.test import TestCase

from users.factories.users_factories import OFMUserFactory

TESTDATA_PATH = 'core/tests/assets'


class PlayerStatisticsParserTest(TestCase):
    def setUp(self):
        testdata = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'), encoding='utf8')
        self.matchday = MatchdayFactory.create()
        user = OFMUserFactory.create()
        season = SeasonFactory.create()

        country_choices = Country.get_choices()
        country_iso_greece = list(country_choices.keys())[list(country_choices.values()).index('Griechenland')]
        nationality_greece, _ = Country.objects.get_or_create(country=country_iso_greece)

        self.player = Player.objects.create(
            id='159883060',
            position='TW',
            name='Chrístos Tsigas',
            birth_season=season,
            nationality=nationality_greece
        )
        self.player = Player.objects.create(
            id='160195494',
            position='LV',
            name='Irwin O\'Canny',
            birth_season=season,
            nationality=nationality_greece
        )
        self.player = Player.objects.create(
            id='159341445',
            position='LMD',
            name='Jan Stemmler',
            birth_season=season,
            nationality=nationality_greece
        )

        self.parser = PlayerStatisticsParser(testdata, user, self.matchday)
        self.player_stat_list = self.parser.parse()
        self.first_player_stat = self.player_stat_list[0]
        self.assertEqual(Matchday.objects.all().count(), 1)

    def test_parsed_player_stat_contains_all_foreign_keys(self):
        self.assertEqual(type(self.first_player_stat), PlayerStatistics)
        self.assertEqual(type(self.first_player_stat.player), Player)
        self.assertEqual(self.first_player_stat.matchday.number, 0)
        self.assertEqual(self.first_player_stat.matchday.season.number, 1)

    def test_parsed_player_stat_contains_all_fields(self):
        self.assertEqual(3, len(self.player_stat_list))
        self.assertEqual('TW', self.first_player_stat.player.position)
        self.assertEqual(159883060, self.first_player_stat.player.id)
        self.assertEqual('Chrístos Tsigas', self.first_player_stat.player.name)
        self.assertEqual('15', self.first_player_stat.strength)
        self.assertEqual('47', self.first_player_stat.freshness)
        self.assertEqual('29', self.first_player_stat.games_in_season)

    def test_parsed_player_stat_contains_correct_scored_goals(self):
        player_stat = self.player_stat_list[2]
        self.assertEqual('4', player_stat.goals_in_season)

    def test_parsed_player_stat_contains_correct_tacklings(self):
        self.assertEqual('32', self.first_player_stat.won_tacklings_in_season)
        self.assertEqual('36', self.first_player_stat.lost_tacklings_in_season)
        self.assertEqual('37', self.first_player_stat.won_friendly_tacklings_in_season)
        self.assertEqual('5', self.first_player_stat.lost_friendly_tacklings_in_season)

    def test_parsed_player_stat_contains_correct_cards_received(self):
        player_stat = self.player_stat_list[1]
        self.assertEqual('3', player_stat.yellow_cards_in_season)
        self.assertEqual('1', player_stat.red_cards_in_season)

    def test_parsed_player_stat_contains_correct_player_enhancement_data(self):
        self.assertEqual('8599', self.first_player_stat.ep)
        self.assertEqual('13227', self.first_player_stat.tp)
        self.assertEqual('10422', self.first_player_stat.awp)

    def test_parsed_player_stat_contains_correct_equity(self):
        self.assertEqual('16015782', self.first_player_stat.equity)

    def test_parse_player_stat_should_return_same_instance_if_nothing_changes(self):
        self.parser.html_source = open(os.path.join(TESTDATA_PATH, 'player_statistics.html'), encoding='utf8')
        stat2 = self.parser.parse()
        self.assertEqual(self.player_stat_list, stat2)
        self.assertEqual(Player.objects.all().count(), 3)
        self.assertEqual(Matchday.objects.all().count(), 1)

    def test_parsed_contract_is_registered(self):
        self.assertEqual(Contract.objects.all().count(), 3)
