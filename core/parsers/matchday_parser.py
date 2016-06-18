from bs4 import BeautifulSoup

from core.models import Matchday, Season
from core.parsers.base_parser import BaseParser
from core.web.ofm_page_constants import Constants


class MatchdayParser(BaseParser):
    def __init__(self):
        self.url = Constants.HEAD

    def parse(self):
        matchday = Matchday()
        matchday.season = Season()
        soup = BeautifulSoup(self.url, "html.parser")
        matchday.number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[0].get_text())
        matchday.season.number = int(soup.body.find_all('div')[1].div.find_all('p')[2].find_all('span')[1].get_text())
        return matchday
