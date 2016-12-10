import logging

from bs4 import BeautifulSoup

from core.models import Match, MatchStadiumStatistics, StadiumLevel, StadiumLevelItem
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class StadiumStatisticsParser(BaseParser):
    def __init__(self, html_source, user, match):
        super(StadiumStatisticsParser, self).__init__()
        self.html_source = html_source
        self.user = user
        self.match = match

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of stadium environment page
        :return: parsed match stadium statidtics
        :rtype: MatchStadiumStatistics
        """

        last_home_matches = Match.objects.filter(user=self.user, stadium_statistics__isnull=False).order_by('matchday')
        last_stadium_level = None
        if last_home_matches.count() > 0:
            # only consider matches statistics BEFORE current match
            last_home_matches = [match for match in last_home_matches if
                                 match.matchday.number <= self.match.matchday.number]
            last_home_match = last_home_matches[0]
            last_stadium_level = MatchStadiumStatistics.objects.filter(match=last_home_match)[0].level

        stadium_items = soup.find('table', id='stadiumExtra').tbody.find_all('tr')
        light_row = stadium_items[0]
        screen_row = stadium_items[1]
        security_row = stadium_items[2]
        parking_row = stadium_items[3]

        if self._is_under_construction(light_row) and last_stadium_level:
            light = last_stadium_level.light
        else:
            light = self._create_stadium_level_item_from_row(light_row)

        if self._is_under_construction(screen_row) and last_stadium_level:
            screen = last_stadium_level.screen
        else:
            screen = self._create_stadium_level_item_from_row(screen_row)

        if self._is_under_construction(security_row) and last_stadium_level:
            security = last_stadium_level.security
        else:
            security = self._create_stadium_level_item_from_row(security_row)

        if self._is_under_construction(parking_row) and last_stadium_level:
            parking = last_stadium_level.parking
        else:
            parking = self._create_stadium_level_item_from_row(parking_row)

        stadium_level, _ = StadiumLevel.objects.get_or_create(
            light=light,
            screen=screen,
            security=security,
            parking=parking
        )

        match_stadium_stat, _ = MatchStadiumStatistics.objects.get_or_create(
            match=self.match,
            level=stadium_level
        )

        return match_stadium_stat

    @staticmethod
    def _is_under_construction(stadium_attribute):
        return stadium_attribute.find_all('td')[1].img is not None and \
               'underconst' in stadium_attribute.find_all('td')[1].img['src']

    @staticmethod
    def _create_stadium_level_item_from_row(row):
        stadium_level_item, _ = StadiumLevelItem.objects.get_or_create(
            current_level=row.find_all('td')[2].span.get_text(),
            value=BaseParser.strip_euro_sign(row.find_all('td')[4].span.get_text().replace('.', '').strip()),
            daily_costs=BaseParser.strip_euro_sign(row.find_all('td')[5].span.get_text().replace('.', '').strip())
        )

        return stadium_level_item
