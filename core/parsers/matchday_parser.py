import logging

from bs4 import BeautifulSoup

from core.models import Matchday, Season
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class MatchdayParser(BaseParser):
    def __init__(self, html_source):
        super(MatchdayParser, self).__init__()
        self.html_source = html_source

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        matchday_number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[0].get_text())
        matchday_season_number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[1].get_text())

        season, _ = Season.objects.get_or_create(
            number=matchday_season_number,
        )

        matchday, _ = Matchday.objects.get_or_create(
            number=matchday_number,
            season=season,
        )

        matchday.season.save()
        matchday.save()
        logger.debug('===== Matchday parsed: %s', matchday)

        return matchday
