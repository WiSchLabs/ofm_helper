from player_statistics.parsers.base_parser import BaseParser
from bs4 import BeautifulSoup


class PlayerStatisticsHtmlParser(BaseParser):
    def parse(self, page):
        soup = BeautifulSoup(page, "html.parser")
        return soup
