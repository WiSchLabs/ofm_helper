from bs4 import BeautifulSoup

from core.models import Matchday, Finance
from core.parsers.base_parser import BaseParser
import logging

logger = logging.getLogger(__name__)


class FinancesParser(BaseParser):
    def __init__(self, html_source, user):
        self.html_source = html_source
        self.user = user

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of finances page
        :return: parsed finances
        :rtype: list
        """
        matchday = Matchday.objects.all()[0]

        finance_table = soup.find(id="einaus").find_all('table')[2]
        finance_values = finance_table.find_all('tr')
        balance = self._int_from_money(finance_values[25].find_all('td')[5].get_text())

        income_visitors_league = self._int_from_money(finance_values[4].find_all('td')[3].div.get_text())
        income_sponsoring = self._int_from_money(finance_values[5].find_all('td')[3].div.get_text())
        income_cup = self._int_from_money(finance_values[6].find_all('td')[3].div.get_text())
        income_interests = self._int_from_money(finance_values[7].find_all('td')[3].div.get_text())
        income_loan = self._int_from_money(finance_values[8].find_all('td')[3].div.get_text())
        income_transfer = self._int_from_money(finance_values[9].find_all('td')[3].div.get_text())
        income_visitors_friendlies = self._int_from_money(finance_values[10].find_all('td')[3].div.get_text())
        income_friendlies = self._int_from_money(finance_values[11].find_all('td')[3].div.get_text())
        income_funcup = self._int_from_money(finance_values[12].find_all('td')[3].div.get_text())
        income_betting = self._int_from_money(finance_values[13].find_all('td')[3].div.get_text())

        expenses_player_salaries = self._int_from_money(finance_values[4].find_all('td')[11].div.get_text())
        expenses_stadium = self._int_from_money(finance_values[5].find_all('td')[11].div.get_text())
        expenses_youth = self._int_from_money(finance_values[6].find_all('td')[11].div.get_text())
        expenses_interests = self._int_from_money(finance_values[7].find_all('td')[11].div.get_text())
        expenses_trainings = self._int_from_money(finance_values[8].find_all('td')[11].div.get_text())
        expenses_transfer = self._int_from_money(finance_values[9].find_all('td')[11].div.get_text())
        expenses_compensation = self._int_from_money(finance_values[10].find_all('td')[11].div.get_text())
        expenses_friendlies = self._int_from_money(finance_values[11].find_all('td')[11].div.get_text())
        expenses_funcup = self._int_from_money(finance_values[12].find_all('td')[11].div.get_text())
        expenses_betting = self._int_from_money(finance_values[13].find_all('td')[11].div.get_text())

        finances, success = Finance.objects.get_or_create(
            user=self.user,
            matchday=matchday,
        )
        logger.debug('===== Finance parsed: %s' % finances)

        finances.balance = balance
        finances.income_visitors_league = income_visitors_league
        finances.income_sponsoring = income_sponsoring
        finances.income_cup = income_cup
        finances.income_interests = income_interests
        finances.income_loan = income_loan
        finances.income_transfer = income_transfer
        finances.income_visitors_friendlies = income_visitors_friendlies
        finances.income_friendlies = income_friendlies
        finances.income_funcup = income_funcup
        finances.income_betting = income_betting
        finances.expenses_player_salaries = expenses_player_salaries
        finances.expenses_stadium = expenses_stadium
        finances.expenses_youth = expenses_youth
        finances.expenses_interests = expenses_interests
        finances.expenses_trainings = expenses_trainings
        finances.expenses_transfer = expenses_transfer
        finances.expenses_compensation = expenses_compensation
        finances.expenses_friendlies = expenses_friendlies
        finances.expenses_funcup = expenses_funcup
        finances.expenses_betting = expenses_betting

        finances.save()

        return finances

    def _int_from_money(self, money):
        return self.strip_euro_sign(money.replace('.', '').strip())

    def strip_euro_sign(self, money):
        return money[:-2]
