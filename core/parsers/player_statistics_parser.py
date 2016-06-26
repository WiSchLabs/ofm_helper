from bs4 import BeautifulSoup

from core.models import Player, PlayerStatistics, Matchday, Season
from core.parsers.base_parser import BaseParser
from core.web.ofm_page_constants import Constants

MULTIVALUE_SEPARATOR = ' / '


class PlayerStatisticsParser(BaseParser):
    def __init__(self):
        self.url = Constants.TEAM.PLAYER_STATISTICS

    def parse(self):
        soup = BeautifulSoup(self.url, "html.parser")
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
        position = player_stat_values[1].get_text()
        name = player_stat_values[2].a.get_text().strip('\n').strip('\t').strip(' ')
        matchday = Matchday.objects.all()[0]
        age = int(player_stat_values[3].get_text())
        birth_season, success = Season.objects.get_or_create(number=matchday.season.number - age)

        player, success = Player.objects.get_or_create(position=position, name=name, birthSeason=birth_season)
        return player

    def _get_value_from_multivalue_table_cell(self, field, index):
        return field.get_text().split(MULTIVALUE_SEPARATOR)[index]

    def _get_ep_tp_value_from_table_cell(self, field):
        return field.get_text().strip('\n').split('\n')[0].strip('\n').strip('\t').replace('.', '')

    def _get_equity_value_from_table_cell(self, field):
        return field.get_text().strip('\n').strip('\t').replace('.', '').replace('€', '').strip(' ')

    def _filter_invalid_cells(self, table_cells):
        import re
        counter_cell_pattern = re.compile(r'<td>[0-9]+</td>')
        return [cell for cell in table_cells
                if str(cell).replace(' ', '').replace('\t', '').replace('\n', '') != '<td>??</td>' and not
                counter_cell_pattern.match(str(cell))]
