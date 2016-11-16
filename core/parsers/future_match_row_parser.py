import logging

from bs4 import BeautifulSoup

from core.models import Matchday, Match, MatchTeamStatistics
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class FutureMatchRowParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        return self.parse_html(self.html_source)

    def parse_html(self, row):
        """
        :param row: BeautifulSoup of match table row
        :return: parsed match
        :rtype: Match
        """

        # we assume to have parsed the season beforehand (with the matchday)
        season = Matchday.objects.all()[0].season
        matchday_number = row.find_all('td')[0].get_text()
        matchday, success = Matchday.objects.get_or_create(season=season, number=matchday_number)

        is_home_match = "black" in row.find_all('td')[1].a.get('class')

        home_team = row.find_all('td')[1].get_text().strip()
        home_team_name = home_team[0:home_team.find('(')-1]
        home_team_strength = home_team[home_team.find('(')+1:home_team.find(')')]

        guest_team = row.find_all('td')[3].get_text().strip()
        guest_team_name = guest_team[0:guest_team.find('(')-1]
        guest_team_strength = guest_team[guest_team.find('(')+1:guest_team.find(')')]

        home_team_stat, success = MatchTeamStatistics.objects.get_or_create(
            team_name=home_team_name,
            strength=home_team_strength,
            ball_possession=0,
            chances=0,
            yellow_cards=0,
            red_cards=0
        )

        guest_team_stat, success = MatchTeamStatistics.objects.get_or_create(
            team_name=guest_team_name,
            strength=guest_team_strength,
            ball_possession=0,
            chances=0,
            yellow_cards=0,
            red_cards=0
        )

        match, success = Match.objects.get_or_create(
            matchday=matchday,
            is_home_match=is_home_match,
            user=self.user,
            home_team_statistics=home_team_stat,
            guest_team_statistics=guest_team_stat
        )

        return match
