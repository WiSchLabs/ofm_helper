import logging

from bs4 import BeautifulSoup

from core.models import Player, PlayerStatistics, Contract
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)

MULTIVALUE_SEPARATOR = '/'


class PlayerStatisticsParser(BaseParser):
    def __init__(self, html_source, user, matchday):
        super(PlayerStatisticsParser, self).__init__()
        self.html_source = html_source
        self.user = user
        self.matchday = matchday

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of player statistics page
        :return: list of parsed player statistics
        :rtype: list
        """
        players_stat_table = soup.find(id="playersStatisticsTable").tbody
        player_list = players_stat_table.find_all('tr')  # 1 row per player

        return [self.parse_row(player_row) for player_row in player_list]

    def parse_row(self, player_row):
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

        parsed_player_stat, _ = PlayerStatistics.objects.get_or_create(
            matchday=self.matchday,
            player=player
        )
        logger.debug('===== PlayerStatistics parsed: %s', parsed_player_stat)

        parsed_player_stat.strength = strength
        parsed_player_stat.games_in_season = games_in_season
        parsed_player_stat.freshness = freshness
        parsed_player_stat.goals_in_season = goals_in_season
        parsed_player_stat.won_tacklings_in_season = won_tacklings_in_season
        parsed_player_stat.lost_tacklings_in_season = lost_tacklings_in_season
        parsed_player_stat.won_friendly_tacklings_in_season = won_friendly_tacklings_in_season
        parsed_player_stat.lost_friendly_tacklings_in_season = lost_friendly_tacklings_in_season
        parsed_player_stat.yellow_cards_in_season = yellow_cards_in_season
        parsed_player_stat.red_cards_in_season = red_cards_in_season
        parsed_player_stat.ep = ep
        parsed_player_stat.tp = tp
        parsed_player_stat.awp = awp
        parsed_player_stat.equity = equity

        parsed_player_stat.save()

        return parsed_player_stat

    def _parse_player(self, player_stat_values):
        ofm_id = player_stat_values[2].a['href'].split('/player/')[1].split('-')[0]

        # we assume to have parsed the players beforehand
        player = Player.objects.get(id=ofm_id)
        self._create_contract(player)

        return player

    def _create_contract(self, player):
        existing_contracts = Contract.objects.filter(player=player, user=self.user, sold_on_matchday=None)
        if existing_contracts.count() > 0:
            contract = existing_contracts[0]
        else:
            contract, _ = Contract.objects.get_or_create(
                player=player,
                user=self.user,
                bought_on_matchday=self.matchday
            )
        return contract

    @staticmethod
    def _get_value_from_multivalue_table_cell(field, index):
        return field.get_text().split(MULTIVALUE_SEPARATOR)[index].strip()

    @staticmethod
    def _get_ep_tp_value_from_table_cell(field):
        return field.get_text().strip('\n').split('\n')[0].strip('\n').strip('\t').replace('.', '')

    def _get_equity_value_from_table_cell(self, field):
        return self.strip_euro_sign(field.get_text().strip('\n').replace('\t', '').replace('.', '').strip(' '))
