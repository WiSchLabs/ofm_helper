from bs4 import BeautifulSoup

from player_statistics.parsers.base_parser import BaseParser
from player_statistics.models import Player, PlayerStatistics


class PlayerStatisticsHtmlParser(BaseParser):
    def parse(self, page):
        soup = BeautifulSoup(page, "html.parser")
        return self.parse_player_statistics_html(soup)

    def parse_player_statistics_html(self, soup: BeautifulSoup) -> PlayerStatistics:
        """
        :param soup: BeautifulSoup of player statistics page
        :return: parsed player statistics
        :rtype: PlayerStatistics
        """
        parsed_player_stat_list = []
        players_stat_table = soup.find(id="playersStatisticsTable").tbody

        # 1 row per player
        player_list = players_stat_table.find_all('tr')
        for player_row in player_list:
            parsed_player_stat = self.parse_player_stat_row(player_row)
            parsed_player_stat_list.append(parsed_player_stat)

        return parsed_player_stat_list

    def parse_player_stat_row(self, player_row):
        parsed_player_stat = PlayerStatistics()
        player_stat_values = player_row.find_all('td')

        parsed_player_stat.strength = player_stat_values[5].get_text().strip(' ')
        parsed_player_stat.freshness = player_stat_values[6].get_text()
        parsed_player_stat.games_in_season = player_stat_values[7].get_text()
        parsed_player_stat.goals_in_season = player_stat_values[8].get_text()

        parsed_player_stat.player = self.parse_player(player_stat_values)

        return parsed_player_stat

    def parse_player(self, player_stat_values):
        parsed_player = Player()
        parsed_player.position = player_stat_values[1].get_text()
        parsed_player.name = player_stat_values[3].a.get_text().strip('\n').strip('\t').strip(' ')
        return parsed_player