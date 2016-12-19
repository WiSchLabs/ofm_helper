import logging

from bs4 import BeautifulSoup

from core.models import Finance
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class FinancesParser(BaseParser):
    def __init__(self, html_source, user, matchday):
        super(FinancesParser, self).__init__()
        self.html_source = html_source
        self.user = user
        self.matchday = matchday

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of finances page
        :return: parsed finances
        :rtype: list
        """

        finance_table = soup.find(id="einaus").find_all('table')[2]
        finance_values = finance_table.find_all('tr')

        finances, _ = Finance.objects.get_or_create(
            user=self.user,
            matchday=self.matchday,
        )
        logger.debug('===== Finance parsed: %s', finances)

        finances.balance = self._int_from_money(finance_values[25].find_all('td')[5].get_text())

        finances.income_visitors_league = self._int_from_money(finance_values[4].find_all('td')[3].div.get_text())
        finances.income_sponsoring = self._int_from_money(finance_values[5].find_all('td')[3].div.get_text())
        finances.income_cup = self._int_from_money(finance_values[6].find_all('td')[3].div.get_text())
        finances.income_interests = self._int_from_money(finance_values[7].find_all('td')[3].div.get_text())
        finances.income_loan = self._int_from_money(finance_values[8].find_all('td')[3].div.get_text())
        finances.income_transfer = self._int_from_money(finance_values[9].find_all('td')[3].div.get_text())
        finances.income_visitors_friendlies = self._int_from_money(finance_values[10].find_all('td')[3].div.get_text())
        finances.income_friendlies = self._int_from_money(finance_values[11].find_all('td')[3].div.get_text())
        finances.income_funcup = self._int_from_money(finance_values[12].find_all('td')[3].div.get_text())
        finances.income_betting = self._int_from_money(finance_values[13].find_all('td')[3].div.get_text())

        finances.expenses_player_salaries = self._int_from_money(finance_values[4].find_all('td')[11].div.get_text())
        finances.expenses_stadium = self._int_from_money(finance_values[5].find_all('td')[11].div.get_text())
        finances.expenses_youth = self._int_from_money(finance_values[6].find_all('td')[11].div.get_text())
        finances.expenses_interests = self._int_from_money(finance_values[7].find_all('td')[11].div.get_text())
        finances.expenses_trainings = self._int_from_money(finance_values[8].find_all('td')[11].div.get_text())
        finances.expenses_transfer = self._int_from_money(finance_values[9].find_all('td')[11].div.get_text())
        finances.expenses_compensation = self._int_from_money(finance_values[10].find_all('td')[11].div.get_text())
        finances.expenses_friendlies = self._int_from_money(finance_values[11].find_all('td')[11].div.get_text())
        finances.expenses_funcup = self._int_from_money(finance_values[12].find_all('td')[11].div.get_text())
        finances.expenses_betting = self._int_from_money(finance_values[13].find_all('td')[11].div.get_text())

        finances.save()

        return finances

    def _int_from_money(self, money):
        return self.strip_euro_sign(money.replace('.', '').strip())
