import logging

from bs4 import BeautifulSoup

from core.models import Matchday, Match, MatchTeamStatistics
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class NotTakenPlaceMatchParser(BaseParser):
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

        row = soup.find(id='table_head').find_all('b')[0].find_parent('tr')
        is_home_match = "<b>" in str(row.find_all('td')[2].a)

        match_result = row.find_all('font', class_='erganz')[0].get_text().strip()
        home_team_score = match_result.split(':')[0]
        guest_team_score = match_result.split(':')[1]

        home_team = row.find_all('b')[0].find_parent('tr').find_all('td')[2].get_text().strip()
        home_team_name = home_team[0:home_team.find('(')-1]
        home_team_strength = home_team[home_team.find('(')+1:home_team.find(')')]

        guest_team = row.find_all('b')[0].find_parent('tr').find_all('td')[7].get_text().strip()
        guest_team_name = guest_team[0:guest_team.find('(')-1]
        guest_team_strength = guest_team[guest_team.find('(')+1:guest_team.find(')')]

        home_team_stat, success = MatchTeamStatistics.objects.get_or_create(
            score=home_team_score,
            team_name=home_team_name,
            strength=home_team_strength,
            ball_possession=100,
            chances=0,
            yellow_cards=0,
            red_cards=0
        )

        guest_team_stat, success = MatchTeamStatistics.objects.get_or_create(
            score=guest_team_score,
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
