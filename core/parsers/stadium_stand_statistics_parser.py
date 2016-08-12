import logging

from bs4 import BeautifulSoup

from core.models import Match, MatchStadiumStatistics, StadiumStandStatistics, StandLevel
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class StadiumStandStatisticsParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

        # we assume to have parsed the match beforehand
        match = Match.objects.filter(user=self.user).order_by('matchday')[0]
        self.match_stadium_stat = MatchStadiumStatistics.objects.filter(match=match)[0]

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of stadium overview page
        :return: parsed stadium stand statistics
        :rtype: list of StadiumStandStatistics
        """

        stadium_stands = soup.find_all('div', class_='ticket-mode')

        return [self._parse_stand_statistics(stand_data) for stand_data in stadium_stands]

    def _parse_stand_statistics(self, stand_data):
        has_roof = 'überdacht' in stand_data.find('h1').get_text()
        has_seats = 'Sitzplätze' in stand_data.find('h1').get_text()
        capacity = stand_data.find_all('tr')[2].find_all('td')[3].div.get_text().replace('.', '')

        stand_level, success = StandLevel.objects.get_or_create(
            capacity=capacity,
            has_roof=has_roof,
            has_seats=has_seats
        )

        sector = stand_data.find('span', class_='white').get_text()[0]
        condition = stand_data.find_all('tr')[2].find_all('td')[0].find_all('span')[1].get_text().replace(',', '.').replace('%', '')
        visitors = stand_data.find_all('tr')[3].find_all('td')[2].span.get_text().replace('.', '')
        ticket_price = stand_data.find_all('tr')[6].find_all('select')[0].find('option', selected=True).get('value')

        stadium_stand_stat, success = StadiumStandStatistics.objects.get_or_create(
            stadium_statistics=self.match_stadium_stat,
            sector=sector,
            visitors=visitors,
            ticket_price=ticket_price,
            condition=condition,
            level=stand_level
        )

        return stadium_stand_stat
