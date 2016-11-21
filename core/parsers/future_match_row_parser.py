import logging

from bs4 import BeautifulSoup
from django.core.exceptions import MultipleObjectsReturned

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
        matchday_number = row.find_all('td')[0].get_text().replace('\n', '')
        matchday, _ = Matchday.objects.get_or_create(season=season, number=matchday_number)

        is_home_match = "black" in row.find_all('td')[1].a.get('class')

        home_team = row.find_all('td')[1].get_text().strip()
        home_team_name = home_team[0:home_team.find('(')-1]
        home_team_strength = home_team[home_team.find('(')+1:home_team.find(')')]

        guest_team = row.find_all('td')[3].get_text().strip()
        guest_team_name = guest_team[0:guest_team.find('(')-1]
        guest_team_strength = guest_team[guest_team.find('(')+1:guest_team.find(')')]

        existing_match = Match.objects.filter(matchday=matchday, user=self.user)

        if len(existing_match) == 1:
            match = existing_match[0]

            match.home_team_statistics.team_name = home_team_name
            match.home_team_statistics.strength = home_team_strength
            match.home_team_statistics.save()

            match.guest_team_statistics.team_name = guest_team_name
            match.guest_team_statistics.strength = guest_team_strength
            match.guest_team_statistics.save()
        elif len(existing_match) == 0:
            home_team_stat = MatchTeamStatistics.objects.create(
                team_name=home_team_name,
                strength=home_team_strength,
                ball_possession=0,
                chances=0,
                yellow_cards=0,
                red_cards=0
            )

            guest_team_stat = MatchTeamStatistics.objects.create(
                team_name=guest_team_name,
                strength=guest_team_strength,
                ball_possession=0,
                chances=0,
                yellow_cards=0,
                red_cards=0
            )

            match = Match.objects.create(
                matchday=matchday,
                is_home_match=is_home_match,
                user=self.user,
                home_team_statistics=home_team_stat,
                guest_team_statistics=guest_team_stat
            )
        else:
            raise MultipleObjectsReturned('There are multiple games on matchday: {}'.format(matchday))

        return match
