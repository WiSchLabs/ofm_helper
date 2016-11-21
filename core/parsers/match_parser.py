import logging

from bs4 import BeautifulSoup
from django.core.exceptions import MultipleObjectsReturned

from core.models import Matchday, Match, MatchTeamStatistics
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class MatchParser(BaseParser):
    def __init__(self, html_source, user, is_home_match):
        self.html_source = html_source
        self.user = user
        self.is_home_match = is_home_match

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of match page
        :return: parsed match
        :rtype: Match
        """

        # we assume to have parsed the season beforehand (via matchday)
        season = Matchday.objects.all()[0].season
        matchday_number = soup.find_all('tbody')[2].find_all('b')[0].get_text().split(',')[1].split('.')[0].strip()
        matchday, success = Matchday.objects.get_or_create(season=season, number=matchday_number)

        venue = soup.find_all('em')[1].get_text()
        match_result = soup.find_all('table')[5].find_all('tr')[0].find_all('td')[3].div.font.get_text()
        home_team_score = match_result.split(':')[0]
        guest_team_score = match_result.split(':')[1]
        home_team_name = soup.find_all('td', class_='erganz')[0].get_text().strip()
        guest_team_name = soup.find_all('td', class_='erganz')[1].get_text().strip()
        strength = soup.find_all('table')[5].find_all('tr')[5].find_all('b')
        home_team_strength = strength[0].get_text().split(':')[1].strip()
        guest_team_strength = strength[1].get_text().split(':')[1].strip()
        ball_possesions = soup.find_all('table')[5].find_all('tr')[6].find_all('b')
        home_team_ball_possession = ball_possesions[0].get_text().replace(',', '.').replace('%', '').strip()
        guest_team_ball_possession = ball_possesions[1].get_text().replace(',', '.').replace('%', '').strip()
        chances = soup.find_all('table')[5].find_all('tr')[7].find_all('b')
        home_team_chances = chances[0].get_text().strip()
        guest_team_chances = chances[1].get_text().strip()
        yellow_cards = soup.find_all('table')[5].find_all('tr')[8].find_all('b')
        home_team_yellow_cards = yellow_cards[0].get_text().strip()
        guest_team_yellow_cards = yellow_cards[1].get_text().strip()
        red_cards = soup.find_all('table')[5].find_all('tr')[9].find_all('b')
        home_team_red_cards = red_cards[0].get_text().strip()
        guest_team_red_cards = red_cards[1].get_text().strip()

        existing_match = Match.objects.filter(matchday=matchday, user=self.user)

        if existing_match:
            if len(existing_match) == 1:
                match = existing_match[0]

                match.home_team_statistics.score = home_team_score
                match.home_team_statistics.team_name = home_team_name
                match.home_team_statistics.strength = home_team_strength
                match.home_team_statistics.ball_possession = home_team_ball_possession
                match.home_team_statistics.chances = home_team_chances
                match.home_team_statistics.yellow_cards = home_team_yellow_cards
                match.home_team_statistics.red_cards = home_team_red_cards

                match.guest_team_statistics.score = guest_team_score
                match.guest_team_statistics.team_name = guest_team_name
                match.guest_team_statistics.strength = guest_team_strength
                match.guest_team_statistics.ball_possession = guest_team_ball_possession
                match.guest_team_statistics.chances = guest_team_chances
                match.guest_team_statistics.yellow_cards = guest_team_yellow_cards
                match.guest_team_statistics.red_cards = guest_team_red_cards
            else:
                raise MultipleObjectsReturned('There are multiple games on matchday: {}'.format(matchday))
        else:
            home_team_stat, success = MatchTeamStatistics.objects.get_or_create(
                score=home_team_score,
                team_name=home_team_name,
                strength=home_team_strength,
                ball_possession=home_team_ball_possession,
                chances=home_team_chances,
                yellow_cards=home_team_yellow_cards,
                red_cards=home_team_red_cards
            )

            guest_team_stat, success = MatchTeamStatistics.objects.get_or_create(
                score=guest_team_score,
                team_name=guest_team_name,
                strength=guest_team_strength,
                ball_possession=guest_team_ball_possession,
                chances=guest_team_chances,
                yellow_cards=guest_team_yellow_cards,
                red_cards=guest_team_red_cards
            )

            match, success = Match.objects.get_or_create(
                matchday=matchday,
                is_home_match=self.is_home_match,
                user=self.user,
                home_team_statistics=home_team_stat,
                guest_team_statistics=guest_team_stat
            )

        match.venue = venue
        match.save()
        return match
