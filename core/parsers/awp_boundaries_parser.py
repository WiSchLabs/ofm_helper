from bs4 import BeautifulSoup

from core.models import Matchday, Finance, AwpBoundaries, AwpBoundariesKeyVal
from core.parsers.base_parser import BaseParser
import logging

logger = logging.getLogger(__name__)


class AwpBoundariesParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of awp boundaries forum page
        :return: parsed awp boundaries
        :rtype: AWP Boundaries object
        """
        matchday = Matchday.objects.all()[0]

        boundaries_raw = soup.find_all('pre', 'bbcode_code')[-1]
        boundaries = boundaries_raw.text.split()[2:]

        awp_boundaries, success = AwpBoundaries.objects.get_or_create(matchday=matchday)
        for i in range(26):
            strength = boundaries[i * 4]
            awp = boundaries[i * 4 + 1]
            AwpBoundariesKeyVal.objects.get_or_create(awp_boundaries=awp_boundaries, strength=strength, awp=awp)

        return awp_boundaries

    def _int_from_money(self, money):
        return self.strip_euro_sign(money.replace('.', '').strip())
