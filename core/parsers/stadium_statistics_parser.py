import logging

from bs4 import BeautifulSoup

from core.models import Match, MatchStadiumStatistics, StadiumLevel, StadiumLevelItem
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class StadiumStatisticsParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of stadium environment page
        :return: parsed match stadium statidtics
        :rtype: MatchStadiumStatistics
        """

        # we assume to have parsed the match beforehand
        match = Match.objects.filter(user=self.user)[0]
        
        stadium_items = soup.find('table', id='stadiumExtra').tbody.find_all('tr')
        
        light_row = stadium_items[0]
        screen_row = stadium_items[1]
        security_row = stadium_items[2]
        parking_row = stadium_items[3]

        light = self._create_stadium_level_item_from_row(light_row)
        screen = self._create_stadium_level_item_from_row(screen_row)
        security = self._create_stadium_level_item_from_row(security_row)
        parking = self._create_stadium_level_item_from_row(parking_row)

        stadium_level, success = StadiumLevel.objects.get_or_create(
            light=light,
            screen=screen,
            security=security,
            parking=parking
        )

        match_stadium_stat, success = MatchStadiumStatistics.objects.get_or_create(
            match=match,
            level=stadium_level
        )

        return match_stadium_stat

    def _create_stadium_level_item_from_row(self, row):
        level = row.find_all('td')[2].span.get_text()
        value = row.find_all('td')[4].span.get_text().replace('€', '').replace('.', '').strip()
        daily_costs = row.find_all('td')[5].span.get_text().replace('€', '').replace('.', '').strip()

        stadium_level_item, success = StadiumLevelItem.objects.get_or_create(
            current_level=level,
            value=value,
            daily_costs=daily_costs
        )

        return stadium_level_item
