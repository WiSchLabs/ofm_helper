import logging

from bs4 import BeautifulSoup

from core.models import Player, Season, Country, Contract
from core.parsers.base_parser import BaseParser

logger = logging.getLogger(__name__)


class PlayersParser(BaseParser):
    def __init__(self, html_source, user, matchday):
        super(PlayersParser, self).__init__()
        self.html_source = html_source
        self.user = user
        self.matchday = matchday

    def parse(self):
        soup = BeautifulSoup(self.html_source, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        """
        :param soup: BeautifulSoup of player page
        :return: parsed players
        :rtype: list
        """
        players_table = soup.find(id="playerTable").tbody
        player_list = players_table.find_all('tr')  # 1 row per player
        parsed_players = [self.parse_row(player_row) for player_row in player_list]
        self._mark_sold_players_as_sold(parsed_players)
        return parsed_players

    def parse_row(self, player_row):
        player_values = self._filter_invalid_cells(player_row.find_all('td'))
        ofm_id = player_row.find_all('input', class_='playerid')[0]['value']
        name = player_values[6].a.get_text().replace('\n', '').replace('\t', '').strip(' ')
        position = player_values[5].find_all('span')[1].get_text()
        age = int(player_values[7].get_text())
        birth_season, _ = Season.objects.get_or_create(number=self.matchday.season.number - age)

        displayed_country = player_values[8].get_text().replace('\n', '').replace('\t', '').strip(' ')
        country_name = ''.join([i for i in displayed_country if not i.isdigit()])
        country_choices = dict(Country._meta.get_field('country').choices)
        country_no = list(country_choices.keys())[list(country_choices.values()).index(country_name)]
        nationality, _ = Country.objects.get_or_create(country=country_no)

        player, _ = Player.objects.get_or_create(id=int(ofm_id),
                                                       birth_season=birth_season,
                                                       nationality=nationality,
                                                       position=position)
        player.name = name
        player.save()

        logger.debug('===== Player parsed: %s', player.name)

        self._create_contract(player)
        logger.debug('===== Contract created.')

        return player

    def _create_contract(self, player):
        existing_contracts = Contract.objects.filter(player=player, user=self.user, sold_on_matchday=None)

        if existing_contracts.count() > 0:
            contract = existing_contracts[0]
        else:
            contract, _ = Contract.objects.get_or_create(
                player=player,
                user=self.user,
                bought_on_matchday=self.matchday
            )

        return contract

    def _mark_sold_players_as_sold(self, parsed_players):
        active_contracts = Contract.objects.filter(user=self.user, sold_on_matchday=None)
        sold_players = list(set([contract.player for contract in active_contracts]) - set(parsed_players))

        for player in sold_players:
            contract = Contract.objects.get(player=player, user=self.user, sold_on_matchday=None)  # latest contract
            contract.sold_on_matchday = self.matchday  # assume today
            contract.save()
