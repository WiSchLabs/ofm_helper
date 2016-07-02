from urllib import request

from bs4 import BeautifulSoup

from core.models import Matchday, Season
from core.parsers.base_parser import BaseParser
from core.web.ofm_page_constants import Constants


class MatchdayParser(BaseParser):
    def __init__(self):
        url = Constants.HEAD
        self.html_source = request.urlopen(url)

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        matchday_number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[0].get_text())
        matchday_season_number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[1].get_text())

        season, season_creation_success = Season.objects.get_or_create(
            number=matchday_season_number,
        )

        matchday, matchday_creation_success = Matchday.objects.get_or_create(
            number=matchday_number,
            season=season,
        )

        matchday.season.save()
        matchday.save()

        return matchday
