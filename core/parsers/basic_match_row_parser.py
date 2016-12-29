import logging

from django.core.exceptions import MultipleObjectsReturned

from core.models import Matchday, Match, MatchTeamStatistics
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class BasicMatchRowParser(BaseParser):
    def __init__(self, html_source, user):
        super(BasicMatchRowParser, self).__init__()
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
        matchday, _ = Matchday.objects.get_or_create(
            season=Matchday.objects.all()[0].season,
            number=row.find_all('td')[0].get_text().replace('\n', '')
        )

        guest_team_score, home_team_score = self._get_team_scores(row)

        home_team = row.find_all('td')[1].get_text().strip()
        home_team_name = home_team[0:home_team.find('(') - 1]
        home_team_strength = home_team[home_team.find('(') + 1:home_team.find(')')]

        guest_team = row.find_all('td')[3].get_text().strip()
        guest_team_name = guest_team[0:guest_team.find('(') - 1]
        guest_team_strength = guest_team[guest_team.find('(') + 1:guest_team.find(')')]

        if len(self._existing_matches(matchday)) == 1:
            match = self._existing_matches(matchday)[0]

            match.home_team_statistics.score = home_team_score
            match.home_team_statistics.team_name = home_team_name
            match.home_team_statistics.strength = home_team_strength
            match.home_team_statistics.save()

            match.guest_team_statistics.score = guest_team_score
            match.guest_team_statistics.team_name = guest_team_name
            match.guest_team_statistics.strength = guest_team_strength
            match.guest_team_statistics.save()
        elif not self._has_existing_matches(matchday):
            home_team_stat = MatchTeamStatistics.objects.create(
                score=home_team_score,
                team_name=home_team_name,
                strength=home_team_strength,
                ball_possession=0,
                chances=0,
                yellow_cards=0,
                red_cards=0
            )

            guest_team_stat = MatchTeamStatistics.objects.create(
                score=guest_team_score,
                team_name=guest_team_name,
                strength=guest_team_strength,
                ball_possession=0,
                chances=0,
                yellow_cards=0,
                red_cards=0
            )

            match = Match.objects.create(
                matchday=matchday,
                is_home_match=self._is_home_match(row),
                user=self.user,
                home_team_statistics=home_team_stat,
                guest_team_statistics=guest_team_stat
            )
        else:
            raise MultipleObjectsReturned('There are multiple games on matchday: {}'.format(matchday))

        return match

    def _has_existing_matches(self, matchday):
        return self._existing_matches(matchday).count() > 0

    def _existing_matches(self, matchday):
        return Match.objects.filter(matchday=matchday, user=self.user)

    @staticmethod
    def _get_team_scores(row):
        match_result = row.find_all('span', class_='erganz')[0].find_parent('tr').get_text().strip()
        home_team_score = match_result.split(':')[0].strip()
        guest_team_score = match_result.split(':')[1].strip()
        if home_team_score == "-" and guest_team_score == "-":
            return 0, 0
        return int(guest_team_score), int(home_team_score)

    @staticmethod
    def _is_home_match(row):
        return "black" in row.find_all('td')[1].a.get('class')
