from bs4 import BeautifulSoup

from core.parsers.base_parser import BaseParser
import logging

logger = logging.getLogger(__name__)


class OfmHelperVersionParser(BaseParser):
    def __init__(self, html_source):
        super(OfmHelperVersionParser, self).__init__()
        self.html_source = html_source

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        version = soup.find_all(class_='tag-references')[0].find_all(class_='css-truncate-target')[0].get_text()
        logger.debug('===== OFM Helper version parsed: %s ', version)

        return version
