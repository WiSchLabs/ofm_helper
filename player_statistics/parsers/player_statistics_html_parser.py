from bs4 import BeautifulSoup

from player_statistics.models import Player, PlayerStatistics
from player_statistics.parsers.base_parser import BaseParser

MULTIVALUE_SEPARATOR = ' / '


class PlayerStatisticsHtmlParser(BaseParser):
    def parse(self, page):
        soup = BeautifulSoup(page, "html.parser")
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
        parsed_player_stat = PlayerStatistics()
        player_stat_values = player_row.find_all('td')

        parsed_player_stat.strength = player_stat_values[5].get_text().strip(' ')
        parsed_player_stat.freshness = player_stat_values[6].get_text()
        parsed_player_stat.games_in_season = player_stat_values[7].get_text()
        parsed_player_stat.goals_in_season = player_stat_values[8].get_text()
        parsed_player_stat.won_tacklings_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[9], 0)
        parsed_player_stat.lost_tacklings_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[9], 1)
        parsed_player_stat.won_friendly_tacklings_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[10], 0)
        parsed_player_stat.lost_friendly_tacklings_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[10], 1)
        parsed_player_stat.yellow_cards_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[13], 0)
        parsed_player_stat.red_cards_in_season = \
            self.get_value_from_multivalue_table_cell(player_stat_values[13], 1)
        parsed_player_stat.ep = self.get_ep_tp_value_from_table_cell(player_stat_values[14])
        parsed_player_stat.tp = self.get_ep_tp_value_from_table_cell(player_stat_values[16])
        parsed_player_stat.awp = player_stat_values[18].span.get_text().replace('.', '')
        parsed_player_stat.equity = self.get_equity_value_from_table_cell(player_stat_values[21])

        parsed_player_stat.player = self.parse_player(player_stat_values)

        return parsed_player_stat

    def parse_player(self, player_stat_values):
        parsed_player = Player()
        parsed_player.position = player_stat_values[1].get_text()
        parsed_player.name = player_stat_values[3].a.get_text().strip('\n').strip('\t').strip(' ')
        return parsed_player

    def get_value_from_multivalue_table_cell(self, field, index):
        return field.get_text().split(MULTIVALUE_SEPARATOR)[index]

    def get_ep_tp_value_from_table_cell(self, field):
        return field.get_text().strip('\n').split('\n')[0].strip('\n').strip('\t').replace('.', '')

    def get_equity_value_from_table_cell(self, field):
        return field.get_text().strip('\n').strip('\t').replace('.', '').replace('€', '').strip(' ')
