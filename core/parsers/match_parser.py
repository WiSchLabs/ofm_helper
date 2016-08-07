import logging

from bs4 import BeautifulSoup

from core.models import Matchday, Match
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class MatchParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of match page
        :return: parsed match
        :rtype: Match
        """

        # we assume to have parsed the matchday beforehand
        matchday = Matchday.objects.all()[0]

        venue = soup.find_all('em')[1].get_text()
        match_result = soup.find_all('table')[5].find_all('tr')[0].find_all('td')[3].div.font.get_text()
        home_goals = match_result.split(':')[0]
        guest_goals = match_result.split(':')[1]
        home_team = soup.find_all('td', class_='erganz')[0].get_text().strip()
        guest_team = soup.find_all('td', class_='erganz')[1].get_text().strip()

        match, success = Match.objects.get_or_create(
            matchday=matchday,
            user=self.user,
            home_goals=home_goals,
            guest_goals=guest_goals,
            venue=venue,
            home_team=home_team,
            guest_team=guest_team
        )

        return match
