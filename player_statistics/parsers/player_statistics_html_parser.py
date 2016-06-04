from bs4 import BeautifulSoup

from player_statistics.parsers.base_parser import BaseParser
from player_statistics.models import Player, PlayerStatistics


class PlayerStatisticsHtmlParser(BaseParser):
    def parse(self, page):
        soup = BeautifulSoup(page, "html.parser")
        player_stat = self.parse_player_statistics(soup)
        return [player_stat]

    @staticmethod
    def parse_player_statistics(soup: BeautifulSoup) -> PlayerStatistics:
        """
        :param soup: BeautifulSoup of player statistics page
        :return: parsed player statistics
        :rtype: PlayerStatistics
        """
        parsed_player_stat = PlayerStatistics()
        parsed_player_stat.player = Player()
        players_stat_table = soup.find(id="playersStatisticsTable").tbody

        # 1 row per player
        player_stat = players_stat_table.find_all('tr')
        player_stat_values = player_stat[0].find_all('td')
        parsed_player_stat.player.position = player_stat_values[1].string

        return parsed_player_stat
