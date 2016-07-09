from bs4 import BeautifulSoup

from core.models import Player, PlayerStatistics, Matchday, Season, PlayerUserOwnership, Country
from core.parsers.base_parser import BaseParser

MULTIVALUE_SEPARATOR = '/'


class PlayerStatisticsParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_player_statistics_html(soup)

    def parse_player_statistics_html(self, soup):
        """
        :param soup: BeautifulSoup of player statistics page
        :return: list of parsed player statistics
        :rtype: list
        """
        players_stat_table = soup.find(id="playersStatisticsTable").tbody
        player_list = players_stat_table.find_all('tr')  # 1 row per player

        return [self.parse_player_stat_row(player_row) for player_row in player_list]

    def parse_player_stat_row(self, player_row):
        # we assume to have parsed the matchday beforehand
        matchday = Matchday.objects.all()[0]
        player_stat_values = self._filter_invalid_cells(player_row.find_all('td'))

        strength = player_stat_values[4].get_text().strip(' ')
        freshness = player_stat_values[5].get_text()
        games_in_season = player_stat_values[6].get_text()
        goals_in_season = player_stat_values[7].get_text()
        won_tacklings_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[8], 0)
        lost_tacklings_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[8], 1)
        won_friendly_tacklings_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[9], 0)
        lost_friendly_tacklings_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[9], 1)
        yellow_cards_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[12], 0)
        red_cards_in_season = \
            self._get_value_from_multivalue_table_cell(player_stat_values[12], 1)
        ep = self._get_ep_tp_value_from_table_cell(player_stat_values[13])
        tp = self._get_ep_tp_value_from_table_cell(player_stat_values[14])
        awp = player_stat_values[15].span.get_text().replace('.', '')
        equity = self._get_equity_value_from_table_cell(player_stat_values[17])

        player = self._parse_player(player_stat_values)

        parsed_player_stat, success = PlayerStatistics.objects.get_or_create(
            matchday=matchday,
            strength=strength,
            freshness=freshness,
            games_in_season=games_in_season,
            goals_in_season=goals_in_season,
            won_tacklings_in_season=won_tacklings_in_season,
            lost_tacklings_in_season=lost_tacklings_in_season,
            won_friendly_tacklings_in_season=won_friendly_tacklings_in_season,
            lost_friendly_tacklings_in_season=lost_friendly_tacklings_in_season,
            yellow_cards_in_season=yellow_cards_in_season,
            red_cards_in_season=red_cards_in_season,
            ep=ep,
            tp=tp,
            awp=awp,
            equity=equity,
            player=player,
        )

        return parsed_player_stat

    def _parse_player(self, player_stat_values):
        ofm_id = player_stat_values[2].a['href'].split('/player/')[1].split('-')[0]

        # we assume to have parsed the matchday beforehand
        matchday = Matchday.objects.all()[0]

        # we assume to have parsed the players beforehand
        player = Player.objects.get(id=ofm_id)

        contract = self._create_player_user_ownership(player, matchday)
        return player

    def _create_player_user_ownership(self, player, matchday):
        existing_contracts = PlayerUserOwnership.objects.filter(player=player, user=self.user, sold_on_matchday=None)
        if existing_contracts.count() > 0:
            contract = existing_contracts[0]
        else:
            contract, success = PlayerUserOwnership.objects.get_or_create(player=player, user=self.user, bought_on_matchday=matchday)
        return contract

    def _get_value_from_multivalue_table_cell(self, field, index):
        return field.get_text().split(MULTIVALUE_SEPARATOR)[index].strip()

    def _get_ep_tp_value_from_table_cell(self, field):
        return field.get_text().strip('\n').split('\n')[0].strip('\n').strip('\t').replace('.', '')

    def _get_equity_value_from_table_cell(self, field):
        return field.get_text().strip('\n').strip('\t').replace('.', '').replace('€', '').strip(' ')
