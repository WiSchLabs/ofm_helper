from bs4 import BeautifulSoup

from core.models import Matchday, Finance
from core.parsers.base_parser import BaseParser


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
        finance = Finance()
        finance.matchday = Matchday.objects.all()[0]
        finance.user = self.user

        finance_table = soup.find(id="einaus").find_all('table')[2]
        finance_values = finance_table.find_all('tr')
        finance.balance = self._int_from_money(finance_values[25].find_all('td')[5].get_text())

        finance.income_visitors_league = self._int_from_money(finance_values[4].find_all('td')[3].div.get_text())
        finance.income_sponsoring = self._int_from_money(finance_values[5].find_all('td')[3].div.get_text())
        finance.income_cup = self._int_from_money(finance_values[6].find_all('td')[3].div.get_text())
        finance.income_interests = self._int_from_money(finance_values[7].find_all('td')[3].div.get_text())
        finance.income_loan = self._int_from_money(finance_values[8].find_all('td')[3].div.get_text())
        finance.income_transfer = self._int_from_money(finance_values[9].find_all('td')[3].div.get_text())
        finance.income_visitors_friendlies = self._int_from_money(finance_values[10].find_all('td')[3].div.get_text())
        finance.income_friendlies = self._int_from_money(finance_values[11].find_all('td')[3].div.get_text())
        finance.income_funcup = self._int_from_money(finance_values[12].find_all('td')[3].div.get_text())
        finance.income_betting = self._int_from_money(finance_values[13].find_all('td')[3].div.get_text())

        finance.expenses_player_salaries = self._int_from_money(finance_values[4].find_all('td')[11].div.get_text())
        finance.expenses_stadium = self._int_from_money(finance_values[5].find_all('td')[11].div.get_text())
        finance.expenses_youth = self._int_from_money(finance_values[6].find_all('td')[11].div.get_text())
        finance.expenses_interests = self._int_from_money(finance_values[7].find_all('td')[11].div.get_text())
        finance.expenses_trainings = self._int_from_money(finance_values[8].find_all('td')[11].div.get_text())
        finance.expenses_transfer = self._int_from_money(finance_values[9].find_all('td')[11].div.get_text())
        finance.expenses_compensation = self._int_from_money(finance_values[10].find_all('td')[11].div.get_text())
        finance.expenses_friendlies = self._int_from_money(finance_values[11].find_all('td')[11].div.get_text())
        finance.expenses_funcup = self._int_from_money(finance_values[12].find_all('td')[11].div.get_text())
        finance.expenses_betting = self._int_from_money(finance_values[13].find_all('td')[11].div.get_text())

        return finance

    def _int_from_money(self, money):
        return money.replace('.', '').replace('€', '').strip()
